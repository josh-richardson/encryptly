from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


@login_required
def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})


def test_themes(request):
    return render(request, "encryptly_backend/private/themes.html", {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))