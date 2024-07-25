
from django.contrib import admin
from django.urls import path,include

from .views import register,login,logout,activate,dashboard,forgetPassword,reset_password_validate,resetPassword

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('forgetPassword/',forgetPassword,name='forgetPassword'),
    path('reset_password_validate/<uidb64>/<token>/',reset_password_validate,name='reset_password_validate'),
    path('resetPassword/',resetPassword,name='resetPassword')
]
