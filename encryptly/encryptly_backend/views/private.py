from django.shortcuts import render


def test_main(request):
    return render(request, "encryptly_backend/private/main.html", {})
