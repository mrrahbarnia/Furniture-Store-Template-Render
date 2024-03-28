"""
Database layer for selecting data
from models which belong to store app.
"""
from typing import TypedDict, NotRequired
from django.db.models import QuerySet, Avg

from store.api.v1.filters import FurnitureFilter
from store.models import (
    Furniture,
    Company,
    Category
)

# =========== Furniture Business logics =========== #
filters_type = TypedDict(
    'filters_type',
    {'name__icontains': NotRequired[str], 'price__range': NotRequired[str]}
)


def list_all_furniture() -> QuerySet[Furniture]:
    """Getting and returning all furniture from database."""
    all_furniture = Furniture.objects.select_related(
        'category', 'company'
    ).only(
        'name', 'price', 'image', 'is_active', 'category_id', 'company_id'
    )
    return all_furniture


def list_active_furniture(
        *, filters: filters_type | None
) -> QuerySet[Furniture]:
    """
    Getting and returning all furniture from database.
    """
    filters = filters or {}

    queryset = Furniture.active.annotate(average_rating=Avg(
        'ratings__rating'
    )).select_related('category', 'company')

    return FurnitureFilter(filters, queryset).qs


# =========== Company Business logics =========== #
def list_active_companies() -> QuerySet[Company]:
    """Listing active companies."""
    active_companies: QuerySet[Company] = Company.active.all().only(
        'name', 'ceo', 'staff'
    )
    return active_companies


def list_all_companies() -> QuerySet[Company]:
    """Listing all companies."""
    all_companies: QuerySet[Company] = Company.objects.all().only(
        'name', 'ceo', 'staff', 'is_active', 'slug'
    )
    return all_companies


# =========== Category Business logics =========== #
def list_active_categories() -> QuerySet[Category]:
    """Listing active categories."""
    active_categories: QuerySet[Category] = Category.active.all()
    return active_categories


def list_all_categories() -> QuerySet[Category]:
    """Listing all categories."""
    all_categories: QuerySet[Category] = Category.objects.all().only(
        'name', 'is_active', 'slug'
    )
    return all_categories
