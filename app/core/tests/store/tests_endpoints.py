"""
Integration testing store app endpoints.
"""
import pytest

from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

FURNITURE_LIST_URL = reverse('store_api:furniture')


class TestPublicEndpoints:
    """
    Test endpoints which dont need a authenticated client.
    """
    def test_listing_furniture_with_unauthenticated_successfully(
            self, furniture_factory, anon_client
    ):
        furniture_factory.create_batch(20)
        response = anon_client.get(FURNITURE_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        # Test pagination
        assert len(response.data['results']) == 10


class TestPrivateEndpoints:
    """
    Test endpoints which need a authenticated client.
    """
    pass
