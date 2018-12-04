from django.contrib.auth.models import User
from django.db import models


class UserTwoFactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    twofactor_enabled = models.BooleanField(default=False, null=False)
    totp_key = models.CharField(max_length=64, default="", null=False)

    def isTwoFactorEnabled(self):
        return self.twofactor_enabled

