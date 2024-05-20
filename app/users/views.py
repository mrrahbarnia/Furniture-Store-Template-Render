from django.shortcuts import render # noqa

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def reset_password(request):
    return render(request, 'users/reset-password.html')

def verify_password(request):
    return render(request, 'users/verify-password.html')

def change_password(request):
    return render(request, 'users/change-password.html')
