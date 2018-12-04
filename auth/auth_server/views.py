import pyotp
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import TwoFactorForm
from .decorators import two_factor_required


def home(request):
    if request.user.is_authenticated:
        return logged(request)
    return render(request, 'auth_server/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth_server/register.html', {'form': form})


def login(request):
    return render(request, 'auth_server/login.html')


@login_required
def two_factor_view(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            # Retrieve user's TOTP key
            user = User.objects.get(username=request.user.username)
            totp = pyotp.TOTP(user.user_two_factor.totp_key)

            if totp.verify(code):
                request.session['twofactor_authenticated'] = True
                request.session.modified = True
                return redirect('home')
            else:
                form = TwoFactorForm()
                return render(request, 'auth_server/twofactor.html', {'form': form, 'error': True})
    else:
        form = TwoFactorForm()
        return render(request, 'auth_server/twofactor.html', {'form': form, 'error': False})


@login_required
def logout_view(request):
    request.session['twofactor_authenticated'] = False
    request.session.modified = True
    logout(request)
    return redirect('home')


@login_required
@two_factor_required
def logged(request):
    return render(request, 'auth_server/logged.html')
