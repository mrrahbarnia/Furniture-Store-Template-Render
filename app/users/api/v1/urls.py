from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import apis

app_name = 'users_api'

urlpatterns = [
    path('register/', apis.RegisterApiView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('change-password/', apis.ChangePasswordApiView.as_view(), name='change_password'),
    path('reset-password/', apis.ResetPasswordApiView.as_view(), name='reset_password'),
    path('verify-password/', apis.VerifyRandPasswordApiView.as_view(), name='verify_password')

]