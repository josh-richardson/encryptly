from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
from django.shortcuts import render

from encryptly_backend.forms import ContactForm


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

    contact_form = ContactForm()
    return render(request, "encryptly_backend/public/contact.html", {"contact_form": contact_form})


def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})
