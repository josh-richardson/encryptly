from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(), max_length=15)
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={'placeholder': "Password"}),
                               max_length=100, )

    class Meta:
        model = User
        fields = ("username", "password")