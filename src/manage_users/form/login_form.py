from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from config.form import AbstractForm
from manage_users.models import AccountUser

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'pnameholder': 'Password'}),
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ('username', 'email', 'password1', 'password2')

