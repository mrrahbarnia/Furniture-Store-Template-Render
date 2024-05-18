# """
# Integration testing store app endpoints.
# """
# import pytest
# import random

# from decimal import Decimal
# from typing import Final
# from django.urls import reverse
# from django.utils import timezone
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.test import APIClient

# from store.models import (
#     Furniture,
#     Company,
#     Category
# )

# pytestmark: Final = pytest.mark.django_db

# # ================ Furniture URL's ================ #
# ACTIVE_FURNITURE_URL: Final[str] = reverse('store_api:active_furniture')
# ALL_FURNITURE_URL: Final[str] = reverse('store_api:furniture')


# def get_furniture_detail_url(*, slug: str) -> str:
#     """Creating and returning a furniture
#     detail url based on it's slug."""
#     return reverse('store_api:furniture_detail', args=[slug])


# def rate_furniture_url(*, slug: str) -> str:
#     """Creating and returning a furniture
#     rating url based on it's slug."""
#     return reverse('store_api:furniture_rate', args=[slug])


# def activate_furniture_url(*, slug: str) -> str:
#     """Creating and returning url for
#     activating furniture by their slug."""
#     return reverse('store_api:activate_furniture', args=[slug])


# def deactivate_furniture_url(*, slug: str) -> str:
#     """Creating and returning url for
#     deactivating furniture by their slug."""
#     return reverse('store_api:deactivate_furniture', args=[slug])


# def delete_furniture_url(*, slug: str) -> str:
#     """Creating and returning url for
#     deleting furniture by their slug."""
#     return reverse('store_api:delete_furniture', args=[slug])


# # ================ Company URL's ================ #
# ALL_COMPANY_URL: Final[str] = reverse('store_api:company')
# ACTIVE_COMPANY_URL: Final[str] = reverse('store_api:active_company')


# def activate_company_url(*, slug: str) -> str:
#     """Creating and returning url for
#     activating companies by their slug."""
#     return reverse('store_api:activate_company', args=[slug])


# def deactivate_company_url(*, slug: str) -> str:
#     """Creating and returning url for
#     deactivating companies by their slug."""
#     return reverse('store_api:deactivate_company', args=[slug])


# # ================ Categories URL's ================ #
# ALL_CATEGORIES_URL: Final[str] = reverse('store_api:categories')
# ACTIVE_CATEGORIES_URL: Final[str] = reverse('store_api:active_categories')


# def activate_category_url(*, slug: str) -> str:
#     """Creating and returning url for
#     activating categories by their slug."""
#     return reverse('store_api:activate_category', args=[slug])


# def deactivate_category_url(*, slug: str) -> str:
#     """Creating and returning url for
#     deactivating categories by their slug."""
#     return reverse('store_api:deactivate_category', args=[slug])


# class TestPublicEndpoints:
#     """
#     Test endpoints which dont need an authenticated client.
#     """
#     def test_listing_furniture_with_unauthenticated_successfully(
#             self, anon_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         furniture_factory.create_batch(20)
#         response: Response = anon_client.get(ACTIVE_FURNITURE_URL)

#         assert response.status_code == status.HTTP_200_OK
#         # Test pagination
#         assert len(response.data['results']) == 10

#     def test_get_furniture_detail(
#             self, anon_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test getting a specific furniture by it's slug
#         and increasing it's views number automatically.
#         """
#         sample_furniture: Furniture = furniture_factory(views=0)
#         url: str = get_furniture_detail_url(slug=sample_furniture.slug)
#         response: Response = anon_client.get(url)

#         sample_furniture.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_furniture.views == 1

#     def test_rate_furniture_unsuccessfully(
#             self, anon_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test rate a specific furniture with
#         unauthenticated user unsuccessfully.
#         """
#         sample_furniture: Furniture = furniture_factory()

#         url: str = rate_furniture_url(slug=sample_furniture.slug)
#         response: Response = anon_client.post(url, {'rate': 8})

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert sample_furniture.ratings.count() == 0

#     def test_filtering_furniture_by_query_params(
#             self, anon_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """Test filtering furniture by query parameters."""
#         furniture_factory(
#             name='Desk', price=Decimal('10.00')
#         )
#         furniture_factory(
#             name='Table', price=Decimal('12.00')
#         )
#         furniture_factory(
#             name='Bed', price=Decimal('15.00')
#         )
#         sample_furniture4: Furniture = furniture_factory(
#             name='Magic Sofa', price=Decimal('28.00')
#         )

#         response: Response = anon_client.get(
#             ACTIVE_FURNITURE_URL, {'name__icontains': 'magi'}
#         )

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['results'][0]['name'] == sample_furniture4.name
#         assert len(response.data['results']) == 1

#         response: Response = anon_client.get(
#             ACTIVE_FURNITURE_URL, {'price__range': '11, 20'}
#         )

#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data['results']) == 2

#     def test_list_active_companies_successfully(
#             self, anon_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test listing active companies
#         by anonymous user successfully.
#         """
#         company_factory.create_batch(20)
#         response: Response = anon_client.get(ACTIVE_COMPANY_URL)

#         assert response.status_code == status.HTTP_200_OK
#         # Test pagination
#         assert len(response.data['results']) == 10

#     def test_list_all_companies_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test listing all companies
#         by anonymous user unsuccessfully.
#         """
#         response: Response = anon_client.get(ALL_COMPANY_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activating_companies_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test activating companies with
#         unauthenticated user unsuccessfully.
#         """
#         url: str = activate_company_url(slug='sample-slug')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivating_companies_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test deactivating companies with
#         unauthenticated user unsuccessfully.
#         """
#         url: str = deactivate_company_url(slug='sample-slug')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_get_all_furniture_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test getting all furniture with
#         anonymous client unsuccessfully.
#         """
#         response: Response = anon_client.get(ALL_FURNITURE_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activating_furniture_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test activating furniture by
#         unauthenticated user unsuccessfully.
#         """
#         url: str = activate_furniture_url(slug='sample-slug')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivating_furniture_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test deactivating furniture by
#         unauthenticated user unsuccessfully.
#         """
#         url: str = deactivate_furniture_url(slug='sample-slug')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_delete_company_anon_client_unsuccessfully(
#             self, anon_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test preventing deleting furniture by unauthenticated users.
#         """
#         sample_company: Company = company_factory()
#         url: str = delete_furniture_url(slug=sample_company.slug)

#         response: Response = anon_client.delete(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert Company.objects.count() == 1, 'The company has been \
#             deleted with anonymous client'

#     def test_list_active_categories_anon_client_successfully(
#             self, anon_client: APIClient, category_factory: Category
#     ):
#         """
#         Test listing active categories by
#         unauthenticated users successfully.
#         """
#         category_factory.create_batch(20)
#         response: Response = anon_client.get(ACTIVE_CATEGORIES_URL)

#         assert response.status_code == status.HTTP_200_OK
#         # Test pagination
#         assert len(
#             response.data['results']
#         ) == 10, "The pagination of active categories does not work."

#     def test_list_all_categories_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ):
#         """
#         Test listing active categories by
#         unauthenticated users successfully.
#         """
#         response: Response = anon_client.get(ALL_CATEGORIES_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activate_category_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ):
#         """
#         Test preventing from activating
#         categories by unauthenticated users.
#         """
#         url: str = activate_category_url(slug='test')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivate_category_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ):
#         """
#         Test preventing from deactivating
#         categories by unauthenticated users.
#         """
#         url: str = deactivate_category_url(slug='test')
#         response: Response = anon_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_create_company_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ):
#         """
#         Test preventing from creating
#         companies with unauthenticated users.
#         """
#         payload: dict = {
#             'name': 'Sample company',
#             'ceo': 'Mr Boss',
#             'staff': 120
#         }
#         response: Response = anon_client.post(ALL_COMPANY_URL, payload)

#         assert response.status_code == status.HTTP_403_FORBIDDEN
    
#     def test_create_furniture_anon_client_unsuccessfully(
#             self, anon_client: APIClient
#     ):
#         """
#         Test preventing from creating
#         furniture by anonymous clients.
#         """
#         response: Response = anon_client.post(ALL_FURNITURE_URL, {})

#         assert response.status_code == status.HTTP_403_FORBIDDEN


# class TestPrivateEndpoints:
#     """
#     Test endpoints which need a authenticated client.
#     """
#     def test_rate_furniture_less_than_0_unsuccessfully(
#             self, normal_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test rate a specific furniture less than 0 unsuccessfully.
#         """
#         sample_furniture: Furniture = furniture_factory()

#         url: str = rate_furniture_url(slug=sample_furniture.slug)
#         response: Response = normal_client.post(url, {'rate': -1})

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert sample_furniture.ratings.count() == 0

#     def test_rate_furniture_successfully(
#             self, normal_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test rate a specific furniture with
#         authenticated user successfully.
#         """
#         sample_furniture: Furniture = furniture_factory()

#         url: str = rate_furniture_url(slug=sample_furniture.slug)
#         response: Response = normal_client.post(url, {'rate': 8})

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_furniture.ratings.count() == 1

#     def test_list_all_companies_with_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ) -> None:
#         """
#         Test listing all companies
#         by normal user unsuccessfully.
#         """
#         response: Response = normal_client.get(ALL_COMPANY_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_list_all_companies_with_admin_client_unsuccessfully(
#             self, admin_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test listing all companies
#         by admin user successfully.
#         """
#         company_factory.create_batch(20, is_active=False)

#         response: Response = admin_client.get(ALL_COMPANY_URL)

#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 20

#     def test_activating_companies_with_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ) -> None:
#         """
#         Test activating companies with
#         normal client unsuccessfully
#         """
#         url: str = activate_company_url(slug='sample-slug')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activating_companies_with_admin_client_successfully(
#             self, admin_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test activating companies with
#         admin client unsuccessfully
#         """
#         sample_company: Company = company_factory(is_active=False)

#         url: str = activate_company_url(slug=sample_company.slug)
#         response: Response = admin_client.get(url)
#         sample_company.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_company.is_active == bool(True)

#     def test_deactivating_companies_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ) -> None:
#         """
#         Test deactivating companies with
#         normal client unsuccessfully.
#         """
#         url: str = deactivate_company_url(slug='test')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivating_companies_admin_client_successfully(
#             self, admin_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test deactivating companies with
#         admin client unsuccessfully.
#         """
#         sample_company: Company = company_factory(is_active=True)

#         url: str = deactivate_company_url(slug=sample_company.slug)
#         response: Response = admin_client.get(url)
#         sample_company.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_company.is_active == bool(False)

#     def test_get_all_furniture_normal_client_unsuccessfully(
#             self, anon_client: APIClient
#     ) -> None:
#         """
#         Test getting all furniture with
#         normal client unsuccessfully.
#         """
#         response: Response = anon_client.get(ALL_FURNITURE_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_get_all_furniture_admin_client_successfully(
#             self, admin_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test getting all furniture with
#         admin client successfully.
#         """
#         furniture_factory.create_batch(
#             20, is_active=random.choice([True, False])
#         )
#         response: Response = admin_client.get(ALL_FURNITURE_URL)

#         assert response.status_code == status.HTTP_200_OK
#         # Test pagination
#         assert len(response.data['results']) == 10, 'Test pagination'

#     def test_activating_furniture_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ) -> None:
#         """
#         Test activating furniture by
#         normal client unsuccessfully.
#         """
#         url: str = activate_furniture_url(slug='sample-slug')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivating_furniture_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ) -> None:
#         """
#         Test activating furniture by
#         normal client unsuccessfully.
#         """
#         url: str = deactivate_furniture_url(slug='sample-slug')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activating_furniture_admin_client_successfully(
#             self, admin_client: APIClient, furniture_factory: Furniture
#     ) -> None:
#         """
#         Test activating furniture by
#         admin client unsuccessfully.
#         """
#         sample_furniture: Furniture = furniture_factory(is_active=False)
#         url: str = activate_furniture_url(slug=sample_furniture.slug)
#         response: Response = admin_client.get(url)
#         sample_furniture.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_furniture.is_active == bool(True)

#     def test_deactivating_furniture_admin_client_successfully(
#             self, admin_client: APIClient, furniture_factory: Furniture
#     ):
#         """
#         Test deactivating furniture by
#         admin client unsuccessfully.
#         """
#         sample_furniture: Furniture = furniture_factory(is_active=True)
#         url: str = deactivate_furniture_url(slug=sample_furniture.slug)
#         response: Response = admin_client.get(url)
#         sample_furniture.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert sample_furniture.is_active == bool(False)

#     def test_delete_company_normal_client_unsuccessfully(
#             self, normal_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test preventing deleting furniture by normal clients.
#         """
#         sample_company: Company = company_factory()
#         url: str = delete_furniture_url(slug=sample_company.slug)

#         response: Response = normal_client.delete(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert Company.objects.count() == 1, 'The company has been \
#             deleted with normal client'

#     def test_delete_company_admin_client_successfully(
#             self, admin_client: APIClient, company_factory: Company
#     ) -> None:
#         """
#         Test deleting companies with admin client successfully.
#         """
#         sample_company: Company = company_factory()
#         url: str = delete_furniture_url(slug=sample_company.slug)

#         response: Response = admin_client.delete(url)

#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert Company.objects.count() == 0

#     def test_list_all_categories_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ):
#         """
#         Test listing all categories by normal users successfully.
#         """
#         response: Response = normal_client.get(ALL_CATEGORIES_URL)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_list_all_categories_admin_client_successfully(
#             self, admin_client: APIClient, category_factory: Category
#     ):
#         """
#         Test listing all categories by admin users successfully.
#         """
#         category_factory.create_batch(
#             20, is_active=random.choice([True, False])
#         )
#         response: Response = admin_client.get(ALL_CATEGORIES_URL)

#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 20

#     def test_activate_category_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ):
#         """
#         Test preventing from activating
#         categories by normal users.
#         """
#         url: str = activate_category_url(slug='test')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_deactivate_category_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ):
#         """
#         Test preventing from deactivating
#         categories by normal users.
#         """
#         url: str = activate_category_url(slug='test')
#         response: Response = normal_client.get(url)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#     def test_activate_category_admin_client_successfully(
#             self, admin_client: APIClient, category_factory: Category
#     ):
#         deactivated_category: Category = category_factory(is_active=False)
#         url: str = activate_category_url(slug=deactivated_category.slug)
#         response: Response = admin_client.get(url)
#         deactivated_category.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert deactivated_category.is_active == bool(True)

#     def test_deactivate_category_admin_client_successfully(
#             self, admin_client: APIClient, category_factory: Category
#     ):
#         activated_category: Category = category_factory(is_active=True)
#         url: str = deactivate_category_url(slug=activated_category.slug)
#         response: Response = admin_client.get(url)
#         activated_category.refresh_from_db()

#         assert response.status_code == status.HTTP_200_OK
#         assert activated_category.is_active == bool(False)

#     def test_create_company_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ):
#         """
#         Test preventing from creating
#         companies with normal clients.
#         """
#         payload: str = {
#             'name': 'Sample company',
#             'ceo': 'Mr Boss',
#             'staff': 120
#         }
#         response: Response = normal_client.post(ALL_COMPANY_URL, payload)

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert Company.objects.filter(
#             name=payload['name']
#         ).exists() == bool(False)

#     def test_create_company_admin_client_unsuccessfully(
#             self, admin_client: APIClient
#     ):
#         """
#         Test preventing from creating
#         companies with admin clients.
#         """
#         payload: str = {
#             'name': 'Sample company',
#             'ceo': 'Mr Boss',
#             'staff': 120
#         }
#         response: Response = admin_client.post(ALL_COMPANY_URL, payload)

#         assert response.status_code == status.HTTP_201_CREATED
#         assert Company.objects.filter(
#             name=payload['name']
#         ).exists() == bool(True), "Company obj hasn't been \
#             created with admin client."
    
#     def test_create_furniture_normal_client_unsuccessfully(
#             self, normal_client: APIClient
#     ):
#         """
#         Test preventing from creating
#         furniture by normal clients.
#         """
#         response: Response = normal_client.post(ALL_FURNITURE_URL, {})

#         assert response.status_code == status.HTTP_403_FORBIDDEN
    
#     def test_create_furniture_with_not_existing_category_unsuccessfully(
#             self, normal_client: APIClient, company_factory: Company
#     ):
#         """
#         Test preventing from creating
#         furniture with not existing category.
#         """
#         sample_company: Company = company_factory()
#         payload: dict = {
#             'name': 'Sample furniture',
#             'price': Decimal(20.20),
#             'stock': 120,
#             'category': 'Wrong category',
#             'company': sample_company.name,
#             'produced_date': timezone.now()
#         }
#         response: Response = normal_client.post(ALL_FURNITURE_URL, payload)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert Furniture.objects.filter(
#             name=payload['name']
#         ).exists == bool(False)

#     def test_create_furniture_with_not_existing_company_unsuccessfully(
#             self, normal_client: APIClient, category_factory: Category
#     ):
#         """
#         Test preventing from creating
#         furniture with not existing company.
#         """
#         sample_category: Category = category_factory()
#         payload: dict = {
#             'name': 'Sample furniture',
#             'price': Decimal(20.20),
#             'stock': 120,
#             'category': sample_category.name,
#             'company': 'Wrong company',
#             'produced_date': timezone.now()
#         }
#         response: Response = normal_client.post(ALL_FURNITURE_URL, payload)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert Furniture.objects.filter(
#             name=payload['name']
#         ).exists == bool(False)

#     def test_create_furniture_successfully(
#             self, normal_client: APIClient,
#             category_factory: Category, company_factory: Company
#     ):
#         sample_company: Company = company_factory()
#         sample_category: Category = category_factory()
#         payload: dict = {
#             'name': 'Sample furniture',
#             'price': Decimal(20.20),
#             'stock': 120,
#             'category': sample_category.name,
#             'company': sample_company.name,
#             'produced_date': timezone.now()
#         }
#         response: Response = normal_client.post(ALL_FURNITURE_URL, payload)

#         assert response.status_code == status.HTTP_201_CREATED
#         assert Furniture.objects.filter(
#             name=payload['name']
#         ).exists == bool(True)
