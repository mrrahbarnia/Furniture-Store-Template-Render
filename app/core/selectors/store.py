"""
Database layer for selecting data
from models which belong to store app.
"""
from typing import TypedDict, NotRequired
from django.db.models import QuerySet, Avg

from store.models import Furniture
from store.api.v1.filters import FurnitureFilter

filters_type = TypedDict(
    'filters_type',
    {'name__icontains': NotRequired[str], 'price__range': NotRequired[str]}
)


def list_active_furniture(
        *, filters: filters_type | None
) -> QuerySet[Furniture]:
    """
    getting and returning all furniture from database.
    """
    filters = filters or {}

    queryset = Furniture.objects.filter(
        is_active=True
    ).annotate(average_rating=Avg(
        'ratings__rating'
    )).select_related('category', 'company')

    return FurnitureFilter(filters, queryset).qs
