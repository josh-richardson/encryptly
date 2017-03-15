import memcache
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from encryptly_backend.forms import ContactForm, UserForm, ProfileForm

client = memcache.Client([('127.0.0.1', 11211)])


def index(request):
    return render(request, "encryptly_backend/public/index.html", {})


def about(request):
    return render(request, "encryptly_backend/public/about.html", {})


def faq(request):
    return render(request, "encryptly_backend/public/faq.html", {})


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.info(request, 'Form submission successful', 'alert-success')
        else:
            messages.info(request, 'The data you submitted was invalid', 'alert-danger')
    else:
        contact_form = ContactForm()
    return render(request, "encryptly_backend/public/contact.html", {"contact_form": contact_form})


def register(request):
    if request.method == 'POST':
        print(request.POST)
        profile_form = ProfileForm(data=request.POST)
        user_form = UserForm(data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
        else:
            print(profile_form.errors)
            print(user_form.errors)

    return render(request, "encryptly_backend/public/register.html", {"profile_form":ProfileForm(), "user_form": UserForm()})


def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})


@csrf_exempt
def user_test(request, test_username):
    client_address_key = "user-check-" + request.META['HTTP_X_FORWARDED_FOR']
    existing_entry = client.get(client_address_key)

    if not existing_entry or int(existing_entry) <= 5:
        client.set(client_address_key, int(existing_entry) + 1, 1600)
        return HttpResponse("true" if User.objects.exists(username=test_username) else "false")
    else:
        return HttpResponse("denied")