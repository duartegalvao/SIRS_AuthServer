from django import forms


class TwoFactorForm(forms.Form):
    code = forms.CharField()

