"""
Fixtures and additional configurations for pytest.
"""
import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


def normal_user():
    pass

def admin_user():
    pass

def anon_client():
    """
    Create and return anonymous
    client without authenticated.
    """
    return APIClient()

def normal_client():
    pass

def admin_client():
    pass