import memcache
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from encryptly_backend.helpers.crypto import encrypt_with_public_key
from encryptly_backend.helpers.twilio import send_text_message
from encryptly_backend.helpers.utils import get_ss_cookie, random_string
from encryptly_backend.models import UserProfile

client = memcache.Client([('127.0.0.1', 11211)])


# CSRF exempt is necessary here as Parsley doesn't know how CSRF works
# This function checks if a given user exists so that parsley can validate the username before the post request is sent.
# It also uses memcached to make sure that the user doesn't flood the server with requests and attempt user enumeration.
@csrf_exempt
def user_exists(request):
    return_dict = {'allowed': False, 'exists': False}
    if request.method == 'POST' and 'username' in request.POST:
        username = request.POST['username']
        if username.isalnum():
            client_address_key = "user-check-" + (request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR'])
            existing_entry = client.get(client_address_key)
            if not existing_entry or int(existing_entry) <= 5:
                return_dict['allowed'] = True
                client.set(client_address_key, int(existing_entry) + 1 if existing_entry else 1, 60)
                if User.objects.filter(username=username).count() != 0: return_dict['exists'] = True
    return JsonResponse(return_dict)


# I realize that this function is ugly. At this point I'm more concerned with getting the app done than writing pretty code. I'll refactor if there's time.
# A detailed description of the rationale for this function is in the GitHub repository in doc/implementation notes/login_spec.txt
def user_login(request):
    # Declare a dictionary to return as JSON
    return_dict = {'authenticated': False, 'two_factor': False, 'passed_two_factor': False, 'logged_in': False, 'private_key': None, 'public_key': None, 'challenge_phrase': None, 'error_message': None}
    # We only accept POST requests
    if request.method == 'POST':
        # If all these are present, the client is telling us that we're at the first stage of authentication
        if 'username' in request.POST and 'password' in request.POST and 'challenge_response' not in request.POST:
            # Authenticate the user and check if actiev
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                if user.is_active:
                    # If so, we set server side cookies to represent this
                    profile = UserProfile.objects.get(user=user)
                    request.session['authenticated'] = True
                    request.session['require_two_factor'] = profile.two_factor
                    return_dict['authenticated'] = True
                    return_dict['two_factor'] = profile.two_factor

                    # If the user has enabled 2FA, we account for this on the server and send a 2FA code to the user
                    if profile.two_factor:
                        request.session['username'] = user.username
                        send_two_factor(user.username, profile.mobile_number)
                    else:
                        return_dict = generate_challenge(return_dict, profile)
                else:
                    return_dict['error_message'] = "Your user account seems to have been deactivated. Please use the contact form for support."
            else:
                return_dict['error_message'] = "Invalid username or password"
        elif get_ss_cookie(request, 'authenticated') is True and 'two_factor' in request.POST and 'username' in request.POST:
            # If the user has initially authenticated (server side cookie present) and has sent a two-factor string then we set request data accordingly
            # Attempt to get the user's 2FA key from memcached
            user_key = client.get("two_factor_" + request.POST['username'])
            return_dict['authenticated'] = True
            return_dict['two_factor'] = True
            if user_key and user_key == request.POST['two_factor']:
                # If the key exists and matches then the user has passed twofactor, they can proceed to the next login step
                return_dict['passed_two_factor'] = True
                request.session['passed_two_factor'] = True
                # Generate a challenge phrase for the user to prove that they know their decryption key
                return_dict = generate_challenge(return_dict, UserProfile.objects.get(user=User.objects.get(username=get_ss_cookie(request, 'username'))))
            else:
                return_dict['error_message'] = "The two-factor key you entered appears to be invalid or has expired. Please try again or contact support."
        elif get_ss_cookie(request, 'authenticated') is True and 'challenge_response' in request.POST and 'username' in request.POST and 'password' in request.POST and \
                (get_ss_cookie(request, 'passed_two_factor') is True or request.session['require_two_factor'] is False):
            # If the user is authenticated, the username and password are in the POST, and the user either has passed 2FA or doesn't have it enabled:
            correct_response = client.get("challenge_response_" + request.POST['username'])
            if correct_response and correct_response == request.POST['challenge_response']:
                # If the user's challenge response was correct (i.e. the decrypted our challenge response and sent it back to us, authenticate the user and log them in.
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user:
                    if user.is_active:
                        login(request, user)
                        return_dict['logged_in'] = True
                        # Set the theme variable if needed
                        user = UserProfile.objects.get(user=request.user)
                        request.session["theme"] = user.theme
                    else:
                        return_dict['error_message'] = "Your user account seems to have been deactivated. Please use the contact form for support."
                else:
                    return_dict['error_message'] = "Invalid username or password"
            else:
                return_dict['error_message'] = "The decryption key you entered failed verification."
        else:
            return_dict['error_message'] = "You appear to have sent an invalid request of some sort."
    # Return JSON representing the request status
    return JsonResponse(return_dict)


def generate_challenge(return_dict, user_profile):
    # Generate a random challenge string
    challenge_string = random_string(30)
    # Set a memcached key containing that string valid for 10 minutes
    client.set("challenge_response_" + user_profile.user.username, challenge_string, 600)
    # Encrypt the challenge string with the user's plaintext public key - if they can decrypt it then they have decrypted their private key. Then send the user the encrypted random string, their public key, and encrypted private key
    return_dict['challenge_phrase'] = encrypt_with_public_key(challenge_string, user_profile)
    return_dict['private_key'] = user_profile.private_key
    return_dict['public_key'] = user_profile.public_key
    # Encrypt a long random string with the user's public key, hopefully they can decrypt it.
    return return_dict


def send_two_factor(username, mobile_number):
    # Generate a random 6-char string and send it to the user's phone, add it to memcached with a 6-minute expiry for validation
    two_factor_key = random_string(6)
    send_text_message("Your Encryptly two-factor authentication code is: " + two_factor_key, mobile_number)
    client.set("two_factor_" + username, two_factor_key, 600)


@login_required
def set_theme(request, int):
    # Save the user's theme according to their preference.
    user = UserProfile.objects.get(user=request.user)
    user.theme = int
    user.save()
    request.session['theme'] = int
    return render(request, "encryptly_backend/private/edit_profile.html", {})
