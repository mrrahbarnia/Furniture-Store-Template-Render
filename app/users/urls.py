from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-password/', views.verify_password, name='verify_password'),
    path('change-password/', views.change_password, name='change_password')
]
