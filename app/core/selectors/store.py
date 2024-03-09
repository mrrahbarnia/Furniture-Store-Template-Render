"""
Database layer for selecting data
from models which belong to store app.
"""
from django.db.models import QuerySet

from store.models import Furniture


def list_active_furniture() -> QuerySet[Furniture]:
    """
    getting and returning all furniture from database.
    """
    return Furniture.objects.filter(
        is_active=True
    ).select_related('category', 'company')
