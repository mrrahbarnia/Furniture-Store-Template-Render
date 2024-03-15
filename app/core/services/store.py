"""
Database layer for executing some operations on data.
"""
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import APIException

from store.models import (
    Furniture,
    Rating,
    FurnitureRating,
    Company
)
from users.models import BaseUser


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


@transaction.atomic
def rate_furniture(*, user: BaseUser, rate: int, slug: str):
    """
    This business logic execute three queries:
    1 => Create and returning a rating object.
    2 => Getting a specific furniture with a given slug.
    3 => Assign that rating to a specific furniture.
    """
    rating: Rating = Rating.objects.create(user=user, rating=rate)
    furniture = Furniture.objects.get(slug=slug, is_active=True)
    furniture_rate = FurnitureRating(rating=rating, furniture=furniture)
    furniture_rate.full_clean()
    furniture_rate.save()


def activate_company(*, slug: str) -> APIException | None:
    """
    Get a company by it's slug and set
    is_active field to True for it.
    """
    try:
        company: Company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        raise APIException('There is no company with the provided slug.')
    except Company.MultipleObjectsReturned:
        raise APIException(
            'There are more than one company with the provided slug.'
        )
    if company.is_active:
        raise APIException(
            'The provided company has already been activated.'
        )
    company.is_active = ~F('is_active')
    company.save(update_fields=['is_active'])


def deactivate_company(*, slug: str) -> APIException | None:
    """
    Get a company by it's slug and set
    is_active field to False for it.
    """
    try:
        company: Company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        raise APIException('There is no company with the provided slug.')
    except Company.MultipleObjectsReturned:
        raise APIException(
            'There are more than one company with the provided slug.'
        )
    if not company.is_active:
        raise APIException(
            'The provided company has already been deactivated.'
        )
    company.is_active = ~F('is_active')
    company.save(update_fields=['is_active'])
