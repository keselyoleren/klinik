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




class ProfileForm(AbstractForm):
    class Meta:
        model = AccountUser
        fields = ['username', 'email', 'first_name', 'last_name']

class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label=_("Password Baru"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'autofocus': True,
            'class':'form-control'
        }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Konfirmasi Password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class':'form-control'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']
