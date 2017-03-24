from audioop import reverse

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from encryptly_backend.forms import ContactForm, UserForm, ProfileForm
from encryptly_backend.views import api


def index(request):
    return render(request, "encryptly_backend/public/index.html", {})


def about(request):
    return render(request, "encryptly_backend/public/about.html", {})


def faq(request):
    return render(request, "encryptly_backend/public/faq.html", {})


def contact(request):
    # If we get a post request and valid contact form data is sent, save it to the model, otherwise send a blank contact form
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
    # If we get a post request and valid user data and profile data are sent, then we create a new user and notify the user, otherwise we render a blank sign-up form
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST)
        user_form = UserForm(data=request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.info(request, 'Account created successfully. You may now log in!', 'alert-success')
            return redirect("login")
        else:
            print(profile_form.errors)
            print(user_form.errors)

    return render(request, "encryptly_backend/public/register.html", {"profile_form": ProfileForm(), "user_form": UserForm()})


def login(request):
    return render(request, "encryptly_backend/public/login.html")

