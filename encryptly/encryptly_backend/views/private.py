from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})


def test_themes(request):
    return render(request, "encryptly_backend/private/themes.html", {})
