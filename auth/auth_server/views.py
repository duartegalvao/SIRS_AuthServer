import pyotp
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import TwoFactorForm, UserCreationWithCaptcha
from .decorators import two_factor_required


def home(request):
    if request.user.is_authenticated:
        return logged(request)
    return render(request, 'auth_server/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationWithCaptcha(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}! You can now login!')
            return redirect('index')
    else:
        form = UserCreationWithCaptcha()
    return render(request, 'auth_server/register.html', {'form': form})


@ratelimit(key='ip', rate='5/m', method=['POST'])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.error(request, 'Retry limit exceded.')
            return render(request, 'auth_server/login.html', {'form': form})

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username} is logged in!')
                return redirect('index')
        messages.error(request, 'Could not login. User credentials do not match a user.')
        return render(request, 'auth_server/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'auth_server/login.html', {'form': form})


@login_required
def two_factor_view(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            # Retrieve user's TOTP key
            user = User.objects.get(username=request.user.username)
            totp = pyotp.TOTP(user.two_factor.totp_key)
            print("Code " + code)
            print("Last verified code " + user.two_factor.last_verified_token)

            if totp.verify(code, valid_window=1) and code != user.two_factor.last_verified_token:
                user.two_factor.last_verified_token = code
                user.two_factor.save()
                request.session['twofactor_authenticated'] = True
                request.session.modified = True
                return redirect('index')
            else:
                form = TwoFactorForm()
                messages.error(request, 'Code could not be verified. Please make sure you typed the correct code.')
                return render(request, 'auth_server/twofactor.html', {'form': form})
    else:
        form = TwoFactorForm()
        return render(request, 'auth_server/twofactor.html', {'form': form})


@login_required
def logout_view(request):
    request.session['twofactor_authenticated'] = False
    request.session.modified = True
    username = request.user.username

    logout(request)
    messages.success(request, f'{username} successfully logged out!')
    return redirect('index')


@login_required
@two_factor_required
def logged(request):
    return render(request, 'auth_server/logged.html')


# ------ API ------
@api_view(['POST'])
@ratelimit(key='ip', rate='5/m')
def api_login(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return Response({
            "error": "retryLimitExceded"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return Response({
            "error": "badRequest"
        }, status=status.HTTP_400_BAD_REQUEST)

    if username == "" or password == "":
        return Response({
                "error": "badRequest"
             }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
                "error": "wrongCredentials"
             }, status=status.HTTP_400_BAD_REQUEST)

    if user.two_factor.isTwoFactorEnabled():
        return Response({
            "error": "notFirstLogin"
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Generate secret and send to user
    # returns a 16 character base32 secret.
    secret = pyotp.random_base32()

    # Save secret
    user.two_factor.two_factor_enabled = True
    user.two_factor.totp_key = secret
    user.two_factor.save()

    return Response({
        "secret": secret
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@ratelimit(key='ip', rate='5/m')
def api_logout(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return Response({
            "error": "retryLimitExceded"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        username = request.data['username']
        totp_key = request.data['totp_key']
    except KeyError:
        return Response({
            "error": "badRequest"
        }, status=status.HTTP_400_BAD_REQUEST)

    if username == "" or totp_key == "":
        return Response({
                "error": "badRequest"
             }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "error": "wrongCredentials"
        }, status=status.HTTP_400_BAD_REQUEST)

    if user is None or user.two_factor.totp_key != totp_key:
        return Response({
            "error": totp_key
        }, status=status.HTTP_400_BAD_REQUEST)

    # Delete secret
    user.two_factor.two_factor_enabled = False
    user.two_factor.totp_key = ""
    user.two_factor.save()

    return Response({}, status=status.HTTP_200_OK)
