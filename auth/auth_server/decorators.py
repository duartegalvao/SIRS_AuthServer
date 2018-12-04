from django.shortcuts import redirect
from django.contrib.auth.models import User


def two_factor_required(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)

        if user.profile.isTwoFactorEnabled():
            # TODO check if two factor is complete
            return function(request, *args, **kwargs)
        else:
            return function(request, *args, **kwargs)

    return wrap
