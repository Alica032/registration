from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from .models import User


class RegisterForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    MIN_LENGTH = 4

    class Meta:
        model = User
        fields = ["username", "phone", "password1", "password2", "email"]

    def clean_password1(self):
        password = self.data.get("password1")
        validate_password(password)
        if password != self.data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return password

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class PhoneVerificationForm(forms.Form):
    verification_code = forms.IntegerField()

    class Meta:
        fields = [
            "verification_code",
        ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        fields = ["username", "password"]

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again."
            )
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        return user


class ActivateForm(forms.Form):
    is_active = forms.BooleanField()

    class Meta:
        fields = ["is_active"]
