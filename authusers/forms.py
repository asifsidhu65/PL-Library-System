import re

from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

alnum_re = re.compile(r"^\w+$")


class AuthLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    remember = forms.BooleanField(label="Remember Me", required=False)

    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError("This account is inactive.")
        else:
            raise forms.ValidationError("Invalid Username and password. Try again.")
        return self.cleaned_data


class AuthSignupForm(forms.Form):

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    username = forms.CharField(
        label="Username", max_length=30, widget=forms.TextInput(), required=True
    )
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password (again)", required=True, widget=forms.PasswordInput)
    email = forms.EmailField(label="Email", widget=forms.TextInput(), required=True)

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError("Usernames can only contain letters, numbers and underscores.")
        User = get_user_model()
        qs = User.objects.filter(username=self.cleaned_data.get('username'))
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError("This username is already taken. Please choose another.")

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = User.objects.filter(email=value)
        if not qs.exists():
            return value
        raise forms.ValidationError("A user is registered with this email address.")

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError("You must type the same password each time.")
        return self.cleaned_data


class ChangePasswordForm(forms.Form):

    password_current = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label="New Password (again)",
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError("Please type your current password.")
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError("You must type the same password each time.")
        return self.cleaned_data["password_new_confirm"]
