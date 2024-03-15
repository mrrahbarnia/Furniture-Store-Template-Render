"""
Integration testing store app endpoints.
"""
import pytest

from decimal import Decimal
from typing import Final
from django.urls import reverse
from rest_framework import status

from store.models import Furniture, Company

pytestmark: Final = pytest.mark.django_db

FURNITURE_LIST_URL: Final[str] = reverse('store_api:furniture')
ALL_COMPANY_URL: Final[str] = reverse('store_api:company')
ACTIVE_COMPANY_URL: Final[str] = reverse('store_api:active_company')


def get_furniture_detail_url(*, slug: str) -> str:
    """Creating and returning a furniture
    detail url based on it's slug."""
    return reverse('store_api:furniture_detail', args=[slug])


def rate_furniture_url(*, slug: str) -> str:
    """Creating and returning a furniture
    rating url based on it's slug."""
    return reverse('store_api:furniture_rate', args=[slug])


def activate_company_url(*, slug: str) -> str:
    """Creating and returning url for
    activating companies by their slug."""
    return reverse('store_api:activate_company', args=[slug])


def deactivate_company_url(*, slug: str) -> str:
    """Creating and returning url for
    deactivating companies by their slug."""
    return reverse('store_api:deactivate_company', args=[slug])


class TestPublicEndpoints:
    """
    Test endpoints which dont need a authenticated client.
    """
    def test_listing_furniture_with_unauthenticated_successfully(
            self, anon_client, furniture_factory: Furniture
    ) -> None:
        furniture_factory.create_batch(20)
        response = anon_client.get(FURNITURE_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        # Test pagination
        assert len(response.data['results']) == 10

    def test_get_furniture_detail(
            self, anon_client, furniture_factory: Furniture
    ) -> None:
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
            self, anon_client, furniture_factory: Furniture
    ) -> None:
        """
        Test rate a specific furniture with
        unauthenticated user unsuccessfully.
        """
        sample_furniture: Furniture = furniture_factory()

        url: str = rate_furniture_url(slug=sample_furniture.slug)
        response = anon_client.post(url, {'rate': 8})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert sample_furniture.ratings.count() == 0

    def test_filtering_furniture_by_query_params(
            self, anon_client, furniture_factory: Furniture
    ) -> None:
        """Test filtering furniture by query parameters."""
        furniture_factory(
            name='Desk', price=Decimal('10.00')
        )
        furniture_factory(
            name='Table', price=Decimal('12.00')
        )
        furniture_factory(
            name='Bed', price=Decimal('15.00')
        )
        sample_furniture4: Furniture = furniture_factory(
            name='Magic Sofa', price=Decimal('28.00')
        )

        response = anon_client.get(
            FURNITURE_LIST_URL, {'name__icontains': 'magi'}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['name'] == sample_furniture4.name
        assert len(response.data['results']) == 1

        response = anon_client.get(
            FURNITURE_LIST_URL, {'price__range': '11, 20'}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_list_active_companies_successfully(
            self, anon_client, company_factory: Company
    ) -> None:
        """
        Test listing active companies
        by anonymous user successfully.
        """
        company_factory.create_batch(20)
        response = anon_client.get(ACTIVE_COMPANY_URL)

        assert response.status_code == status.HTTP_200_OK
        # Test pagination
        assert len(response.data['results']) == 10

    def test_list_all_companies_anon_client_unsuccessfully(
            self, anon_client
    ) -> None:
        """
        Test listing all companies
        by anonymous user unsuccessfully.
        """
        response = anon_client.get(ALL_COMPANY_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_activating_companies_anon_client_unsuccessfully(
            self, anon_client
    ) -> None:
        """
        Test activating companies with
        unauthenticated user unsuccessfully.
        """
        url: str = activate_company_url(slug='sample-slug')
        response = anon_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deactivating_companies_anon_client_unsuccessfully(
            self, anon_client
    ) -> None:
        """
        Test deactivating companies with
        unauthenticated user unsuccessfully.
        """
        url: str = deactivate_company_url(slug='sample-slug')
        response = anon_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPrivateEndpoints:
    """
    Test endpoints which need a authenticated client.
    """
    def test_rate_furniture_less_than_0_unsuccessfully(
            self, normal_client, furniture_factory
    ) -> None:
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
    ) -> None:
        """
        Test rate a specific furniture with
        authenticated user successfully.
        """
        sample_furniture: Furniture = furniture_factory()

        url: str = rate_furniture_url(slug=sample_furniture.slug)
        response = normal_client.post(url, {'rate': 8})

        assert response.status_code == status.HTTP_200_OK
        assert sample_furniture.ratings.count() == 1

    def test_list_all_companies_with_normal_client_unsuccessfully(
            self, normal_client
    ) -> None:
        """
        Test listing all companies
        by normal user unsuccessfully.
        """
        response = normal_client.get(ALL_COMPANY_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_all_companies_with_admin_client_unsuccessfully(
            self, admin_client, company_factory: Company
    ) -> None:
        """
        Test listing all companies
        by admin user successfully.
        """
        company_factory.create_batch(20, is_active=False)

        response = admin_client.get(ALL_COMPANY_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 20

    def test_activating_companies_with_normal_client_unsuccessfully(
            self, normal_client
    ) -> None:
        """
        Test activating companies with
        normal client unsuccessfully
        """
        url: str = activate_company_url(slug='sample-slug')
        response = normal_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_activating_companies_with_admin_client_successfully(
            self, admin_client, company_factory
    ) -> None:
        """
        Test activating companies with
        admin client unsuccessfully
        """
        sample_company: Company = company_factory(is_active=False)

        url: str = activate_company_url(slug=sample_company.slug)
        response = admin_client.get(url)
        sample_company.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert sample_company.is_active == bool(True)

    def test_deactivating_companies_normal_client_unsuccessfully(
            self, normal_client
    ) -> None:
        """
        Test deactivating companies with
        normal client unsuccessfully.
        """
        url: str = deactivate_company_url(slug='test')
        response = normal_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deactivating_companies_admin_client_successfully(
            self, admin_client, company_factory
    ) -> None:
        """
        Test deactivating companies with
        admin client unsuccessfully.
        """
        sample_company: Company = company_factory(is_active=True)

        url: str = deactivate_company_url(slug=sample_company.slug)
        response = admin_client.get(url)
        sample_company.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert sample_company.is_active == bool(False)
