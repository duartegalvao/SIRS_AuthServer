from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('login/twofactor', views.two_factor_view, name='twofactor'),
    path('logout/', views.logout_view, name='logout')
]