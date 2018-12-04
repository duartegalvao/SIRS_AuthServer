from django.shortcuts import redirect
from django.contrib.auth.models import User


def two_factor_required(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)

        if user.user_two_factor.isTwoFactorEnabled():
            if request.session.get('twofactor_authenticated', False):
                return function(request, *args, **kwargs)
            else:
                return redirect('twofactor')
        else:
            return function(request, *args, **kwargs)

    return wrap
