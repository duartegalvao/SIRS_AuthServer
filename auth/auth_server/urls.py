from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('login/twofactor/', views.two_factor_view, name='twofactor'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', views.api_login, name='api_login'),
    url(r'^captcha/', include('captcha.urls')),
]