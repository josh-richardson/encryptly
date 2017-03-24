from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from encryptly_backend.models import UserProfile
from encryptly_backend.forms import ProfileEditForm
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})

@login_required
def set_theme(request, int):
    user = UserProfile.objects.get(user=request.user)
    user.theme = int
    user.save()
    request.session['theme'] = int
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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        edit_profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return HttpResponseRedirect("/profile/")
    else:
        user = request.user
        profile = user.profile
        form = ProfileEditForm(instance=profile)

    args = {}
    args.update(csrf(request))
    args['user'] = user
    args['form'] = form
    return render(request, 'encryptly_backend/private/edit_profile.html', args)


@login_required
def delete_profile(request):
    usr = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        logout(request)
        usr.delete()
        messages.success(request, "Deleted profile successfully.")
        return redirect('index')

    context = {}
    context['prof'] = profile
    return render(request, 'encryptly_backend/private/delete_profile.html', context)
