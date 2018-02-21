from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('email', 'password1', 'password2', 'github_user_name')
