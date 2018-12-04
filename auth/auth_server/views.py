from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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


def logout_view(request):
    logout(request)
    return redirect('')


@login_required
@two_factor_required
def logged(request):
    return render(request, 'auth_server/logged.html')
