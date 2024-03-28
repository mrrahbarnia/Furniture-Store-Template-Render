"""
Fixtures and additional configurations for pytest.
"""
import pytest
from pytest_factoryboy import register

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from users.models import BaseUser
from .factories import (
    FurnitureFactory,
    MaterialFactory,
    ColorFactory,
    CategoryFactory,
    CompanyFactory,
    FurnitureMaterialFactory,
    FurnitureColorFactory
)

User = get_user_model()

register(FurnitureFactory)
register(MaterialFactory)
register(ColorFactory)
register(CategoryFactory)
register(CompanyFactory)
register(FurnitureColorFactory)
register(FurnitureMaterialFactory)


@pytest.fixture
def anon_client():
    """
    Create and return anonymous
    client without authenticated.
    """
    return APIClient()


@pytest.fixture
def normal_client():
    """
    Create and return authenticated
    client as a normal user.
    """
    client = APIClient()
    user = BaseUser.objects.create_user(
        email='normal@example.com',
        password='1234@example.com'
    )
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client():
    """
    Create and return authenticated
    client as a admin user.
    """
    client = APIClient()
    user = BaseUser.objects.create_superuser(
        email='normal@example.com',
        password='1234@example.com'
    )
    client.force_authenticate(user=user)
    return client
