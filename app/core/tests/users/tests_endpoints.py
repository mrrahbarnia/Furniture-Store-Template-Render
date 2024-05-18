"""
Integration testing users app endpoints.
"""
import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from users.models import BaseUser

LOGIN_URL = reverse('users_api:login')
REGISTER_URL = reverse('users_api:register')

pytestmark = pytest.mark.django_db

class TestPublicEndpoints:
    """
    Test endpoints which don't need an authenticated client.
    """
    def test_login_endpoint_with_not_existing_user(
            self, anon_client: APIClient
    ) -> None:
        payload = {
            'email': 'test@example.com',
            'password': 'test@12345678'
        }
        response: Response = anon_client.post(LOGIN_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_endpoint_with_existing_user(
            self, anon_client: APIClient
    ) -> None:
        user = BaseUser.objects.create_user(email='test@example.com', password='test@12345678')

        payload = {
            'email': user.email,
            'password': 'test@12345678'
        }
        response: Response = anon_client.post(LOGIN_URL, payload)

        assert response.status_code == status.HTTP_200_OK
    
    def test_register_endpoint_with_bad_format_email(
            self, anon_client: APIClient
    ) -> None:
        """
        Test register endpoint with bad format email.
        """
        payload = {
            'email': 'bad_format',
            'password': 'test@12345678',
            'password1': 'test@12345678',
        }
        response: Response = anon_client.post(REGISTER_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert BaseUser.objects.filter(email=payload['email']).exists() == False
    
    def test_register_endpoint_with_bad_format_password(
            self, anon_client: APIClient
    ) -> None:
        """
        Test register endpoint with bad format client.
        """
        payload = {
            'email': 'user@example.com',
            'password': '12345',
            'password1': '12345',
        }
        response: Response = anon_client.post(REGISTER_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['extra']['fields']['password']) == 3
    
    def test_register_endpoint_successfully(self, anon_client: APIClient) -> None:
        """
        Test register endpoint with definition rules successfully.
        """
        payload = {
            'email': 'user@example.com',
            'password': 'user@12345678',
            'password1': 'user@12345678',
        }
        response: Response = anon_client.post(REGISTER_URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert BaseUser.objects.filter(email=payload['email']).exists() == True
