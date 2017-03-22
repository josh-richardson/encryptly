from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from encryptly_backend.models import UserProfile


@login_required
def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})


def test_themes(request):
    return render(request, "encryptly_backend/private/themes.html", {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
@login_required
def user_profile(request):
	profile = UserProfile.objects.get(user=request.user)
	context_dic = {}
	context_dic["username"] = profile.user
	context_dic["2fa"] = profile.two_factor
	context_dic["mobile"] = profile.mobile_number
	context_dic["online"] = profile.online_status
	context_dic["profile_pic"] = profile.profile_picture
	return render(request, "encryptly_backend/private/profile.html", context_dic)

