from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import apis

app_name = 'users_api'

urlpatterns = [
    path('register/', apis.RegisterApiView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login')
]