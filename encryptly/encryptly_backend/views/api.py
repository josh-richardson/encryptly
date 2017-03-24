import memcache
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from encryptly_backend.helpers.crypto import encrypt_with_public_key
from encryptly_backend.helpers.twilio import send_text_message
from encryptly_backend.helpers.utils import get_ss_cookie, random_string
from encryptly_backend.models import UserProfile

client = memcache.Client([('127.0.0.1', 11211)])


# CSRF exempt is necessary here as Parsley doesn't know how CSRF works
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


# I realize that this function is ridiculously inefficient and ugly. At this point I'm more concerned with getting the app done than writing pretty code.
def user_login(request):
    return_dict = {'authenticated': False, 'two_factor': False, 'passed_two_factor': False, 'logged_in': False, 'private_key': None, 'public_key': None, 'challenge_phrase': None, 'error_message': None}
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'challenge_response' not in request.POST:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                if user.is_active:
                    profile = UserProfile.objects.get(user=user)
                    request.session['authenticated'] = True
                    request.session['require_two_factor'] = profile.two_factor
                    return_dict['authenticated'] = True
                    return_dict['two_factor'] = profile.two_factor

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
            user_key = client.get("two_factor_" + request.POST['username'])
            return_dict['authenticated'] = True
            return_dict['two_factor'] = True
            if user_key and user_key == request.POST['two_factor']:
                return_dict['passed_two_factor'] = True
                request.session['passed_two_factor'] = True
                return_dict = generate_challenge(return_dict, UserProfile.objects.get(user=User.objects.get(username=get_ss_cookie(request, 'username'))))
            else:
                return_dict['error_message'] = "The two-factor key you entered appears to be invalid or has expired. Please try again or contact support."
        elif get_ss_cookie(request, 'authenticated') is True and 'challenge_response' in request.POST and 'username' in request.POST and 'password' in request.POST and \
                (get_ss_cookie(request, 'passed_two_factor') is True or request.session['require_two_factor'] is False):
            correct_response = client.get("challenge_response_" + request.POST['username'])
            if correct_response and correct_response == request.POST['challenge_response']:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user:
                    if user.is_active:
                        login(request, user)
                        return_dict['logged_in'] = True
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


    return JsonResponse(return_dict)


def generate_challenge(return_dict, user_profile):

    challenge_string = random_string(30)
    client.set("challenge_response_" + user_profile.user.username, challenge_string, 600)
    return_dict['challenge_phrase'] = encrypt_with_public_key(challenge_string, user_profile)
    return_dict['private_key'] = user_profile.private_key
    return_dict['public_key'] = user_profile.public_key
    # Encrypt a long random string with the user's public key, hopefully they can decrypt it.
    return return_dict


def send_two_factor(username, mobile_number):
    two_factor_key = random_string(6)
    send_text_message("Your Encryptly two-factor authentication code is: " + two_factor_key, mobile_number)
    client.set("two_factor_" + username, two_factor_key, 600)
