from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, "encryptly_backend/index.html", {})


def about(request):
    return render(request, "encryptly_backend/about.html", {})
