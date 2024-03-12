"""
Integration testing store app endpoints.
"""
import pytest

from typing import Final
from django.urls import reverse
from rest_framework import status

from store.models import Furniture

pytestmark: Final = pytest.mark.django_db

FURNITURE_LIST_URL: Final = reverse('store_api:furniture')


def get_furniture_detail_url(*, slug: str) -> str:
    """Creating and returning a furniture
    detail url based on it's slug."""
    return reverse('store_api:furniture_detail', args=[slug])


def rate_furniture_url(*, slug: str) -> str:
    """Creating and returning a furniture
    rating url based on it's slug."""
    return reverse('store_api:furniture_rate', args=[slug])


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

    def test_get_furniture_detail(self, furniture_factory, anon_client):
        """
        Test getting a specific furniture by it's slug
        and increasing it's views number automatically.
        """
        sample_furniture: Furniture = furniture_factory(views=0)
        url: str = get_furniture_detail_url(slug=sample_furniture.slug)
        response = anon_client.get(url)

        sample_furniture.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert sample_furniture.views == 1

    def test_rate_furniture_unsuccessfully(
            self, anon_client, furniture_factory
    ):
        """
        Test rate a specific furniture with
        unauthenticated user unsuccessfully.
        """
        sample_furniture: Furniture = furniture_factory()

        url: str = rate_furniture_url(slug=sample_furniture.slug)
        response = anon_client.post(url, {'rate': 8})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert sample_furniture.ratings.count() == 0


class TestPrivateEndpoints:
    """
    Test endpoints which need a authenticated client.
    """
    def test_rate_furniture_less_than_0_unsuccessfully(
            self, normal_client, furniture_factory
    ):
        """
        Test rate a specific furniture less than 0 unsuccessfully.
        """
        sample_furniture: Furniture = furniture_factory()

        url: str = rate_furniture_url(slug=sample_furniture.slug)
        response = normal_client.post(url, {'rate': -1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert sample_furniture.ratings.count() == 0

    def test_rate_furniture_successfully(
            self, normal_client, furniture_factory
    ):
        """
        Test rate a specific furniture with
        authenticated user successfully.
        """
        sample_furniture: Furniture = furniture_factory()

        url: str = rate_furniture_url(slug=sample_furniture.slug)
        response = normal_client.post(url, {'rate': 8})

        assert response.status_code == status.HTTP_200_OK
        assert sample_furniture.ratings.count() == 1
