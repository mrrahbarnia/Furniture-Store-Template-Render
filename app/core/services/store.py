"""
Database layer for executing some operations on data.
"""
from django.db.models import F

from store.models import Furniture


def get_furniture_by_slug(*, slug: str) -> Furniture:
    """
    Get a specific furniture from database with assigned
    slug and increasing it's views number by one.
    """
    furniture = Furniture.objects.select_related(
        'category', 'company'
    ).filter(slug=slug).first()
    furniture.views = F('views') + 1
    furniture.save(update_fields=['views'])
    return furniture
