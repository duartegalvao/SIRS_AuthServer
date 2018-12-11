from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db import models


class UserTwoFactor(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='two_factor')

    two_factor_enabled = models.BooleanField(default=False, null=False)
    totp_key = models.CharField(max_length=16, default="", null=False)

    def __str__(self):
        return self.user.__str__()

    def isTwoFactorEnabled(self):
        return self.two_factor_enabled
