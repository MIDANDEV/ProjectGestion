from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('dashboard/', views.home, name='home'),
    path('', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.log_out, name='log_out'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('update-password/<str:token>/<str:uid>', views.update_password, name='update_password'),
]
