"""
Integration testing users app endpoints.
"""
import pytest

from unittest.mock import patch
from django.urls import reverse
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from users.models import BaseUser

LOGIN_URL = reverse('users_api:login')
REGISTER_URL = reverse('users_api:register')
CHANGE_PASSWORD_URL = reverse('users_api:change_password')
RESET_PASSWORD = reverse('users_api:reset_password')
VERIFY_PASSWORD_URL = reverse('users_api:verify_password')

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

    def test_change_password_with_unauthenticated_client(
            self, anon_client: APIClient
    ) -> None:
        """
        Test unauthorized permission works change
        user endpoint with unauthenticated user.
        """
        response: Response = anon_client.post(CHANGE_PASSWORD_URL, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['message'] == 'Authentication credentials were not provided.'

    def test_reset_password_with_not_existing_email(
            self, anon_client: APIClient
    ) -> None:
        """
        Test reset password endpoint with given email that not existing in database.
        """
        payload = {
            'email': 'notExisting@gmail.com'
        }
        response: Response = anon_client.post(RESET_PASSWORD, payload)

        assert response.data['message'] == 'Validation Error'
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('core.services.users.cache.set')
    def test_reset_password_with_existing_email_successfully(
            self, mocked_cached_set, anon_client: APIClient
    ) -> None:
        """
        Test reset password endpoint with existing email.
        """
        mocked_cached_set.side_effect = 'rand_pass@12345'
        user = BaseUser.objects.create_user(email='test@example.com', password='test@12345678')
        payload = {
            'email': user.email
        }
        response: Response = anon_client.post(RESET_PASSWORD, payload)

        assert response.status_code == status.HTTP_200_OK


class TestPrivateEndpoints:
    """
    Test endpoints that need authentication.
    """
    def test_change_password_endpoint_with_not_equal_passwords(
            self, normal_client: APIClient
    ) -> None:
        """
        Test failure change password endpoint with two different new passwords.
        """
        payload = {
            'old_password': 'normal@example.com',
            'new_password': 'example@12345678',
            'new_password1': 'different_password',
        }
        response: Response = normal_client.post(CHANGE_PASSWORD_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'Validation Error'

    def test_change_password_endpoint_with_wrong_old_password(
            self, normal_client: APIClient
    ) -> None:
        """
        Test failure change password endpoint with wrong old password.
        """
        payload = {
            'old_password': 'normal@example.com',
            'new_password': 'example@12345678',
            'new_password1': 'example@12345678',
        }
        response: Response = normal_client.post(CHANGE_PASSWORD_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'Validation Error'
    
    def test_change_password_correctly(self, normal_client: APIClient) -> None:
        """Test change password successfully."""
        payload = {
            'old_password': '1234@example.com',
            'new_password': 'example@12345678',
            'new_password1': 'example@12345678',
        }
        response: Response = normal_client.post(CHANGE_PASSWORD_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Password changed successfully'

