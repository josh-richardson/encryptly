from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from chat.forms import UserForm


# @login_required
from chat.models import Contact

@login_required
def index(request):
    return render(request, "chat/index.html", {})


def register(request):
    if request.method == "POST":
        signup_form = UserForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()
        return redirect("login")
    return render(request, "chat/register.html", {"register_form": UserForm()})


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user=user)
            return redirect("index")
    return render(request, "chat/login.html", {})


# @login_required
# def add_contact(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         user = User.objects().get(username=username)
#         if user:
#             contact = Contact()
#             contact.contact1 = request.user
#             contact.contact2 = user
#             contact.save()
