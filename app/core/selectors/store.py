"""
Database layer for selecting data
from models which belong to store app.
"""
from django.db.models import QuerySet, Avg

from store.models import Furniture


def list_active_furniture() -> QuerySet[Furniture]:
    """
    getting and returning all furniture from database.
    """
    return Furniture.objects.filter(
        is_active=True
    ).annotate(average_rating=Avg(
        'ratings__rating'
    )).select_related('category', 'company')
