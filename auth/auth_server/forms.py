from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm


class TwoFactorForm(forms.Form):
    code = forms.CharField()


class UserCreationWithCaptcha(UserCreationForm):
    captcha = CaptchaField()
