"""
Integration testing store app endpoints.
"""
import pytest

pytestmark = pytest.mark.django_db


class TestPublicEndpoints:
    """
    Test endpoints which dont need a authenticated client.
    """
    def tests_sample(self):
        assert 0 == 0


class TestPrivateEndpoints:
    """
    Test endpoints which need a authenticated client.
    """
    pass
