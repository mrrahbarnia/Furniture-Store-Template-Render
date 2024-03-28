"""
Database layer for executing some operations on data.
"""
from django.db import transaction
from django.db.models import F
from django.utils.text import slugify
from rest_framework.exceptions import APIException

from store.models import (
    Furniture,
    Rating,
    FurnitureRating,
    Company,
    Category
)
from users.models import BaseUser


# =========== Furniture Business logics =========== #
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


def activate_furniture(*, slug: str) -> None:
    """
    Get a specific furniture by it's slug and
    turn the is_active field to True for it
    """
    try:
        furniture: Furniture = Furniture.objects.get(slug=slug)
    except Furniture.DoesNotExist:
        raise APIException(
            'There is no furniture with the provided slug.'
        )
    except Furniture.MultipleObjectsReturned:
        raise APIException(
            'There are more than one furniture with the provided slug.'
        )

    if not furniture.is_active:
        """
        Check either the is_active field is already activated or not.
        """
        furniture.is_active = ~F('is_active')
        furniture.save(update_fields=['is_active'])
    else:
        raise APIException(
            'The provided furniture has already been activated.'
        )


def deactivate_furniture(*, slug: str) -> None:
    """
    Get a specific furniture by it's slug and
    turn the is_active field to False for it
    """
    try:
        furniture: Furniture = Furniture.objects.get(slug=slug)
    except Furniture.DoesNotExist:
        raise APIException(
            'There is no furniture with the provided slug.'
        )
    except Furniture.MultipleObjectsReturned:
        raise APIException(
            'There are more than one furniture with the provided slug.'
        )

    if not furniture.is_active:
        """
        Check either the is_active field is already activated or not.
        """
        raise APIException(
            'The provided furniture has already been deactivated.'
        )
    else:
        furniture.is_active = ~F('is_active')
        furniture.save(update_fields=['is_active'])


# =============== Company business logics =============== #
def create_company(
        *, name: str, ceo: str, staff: int
) -> Company:
    """
    Creating company by provided data.
    """
    company: Company = Company.objects.create(
        name=name, slug=slugify(name), ceo=ceo, staff=staff
    )
    # TODO: Sending email to admin users.
    return company


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


def delete_company(*, slug: str) -> None:
    """
    Deleting a specific company with it's slug.
    """
    try:
        Company.objects.get(slug=slug).delete()
    except Company.DoesNotExist:
        raise APIException('There is no company with the provided slug.')
    except Company.MultipleObjectsReturned:
        raise APIException(
            'There are more than one company with the provided slug.'
        )


# =========== Category Business logics =========== #
def activate_category(*, slug: str) -> APIException | None:
    """
    Activating a specific category by it's slug.
    """
    try:
        category: Category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise APIException('There is no category with the provided slug.')
    except Category.MultipleObjectsReturned:
        raise APIException(
            'There are more than one company with the provided slug.'
        )
    if category.is_active:
        raise APIException(
            'The provided category has already been activated.'
        )
    category.is_active = ~F('is_active')
    category.save(update_fields=['is_active'])


def deactivate_category(*, slug: str) -> APIException | None:
    """
    Deactivating a specific category by it's slug.
    """
    try:
        category: Category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise APIException('There is no category with the provided slug.')
    except Category.MultipleObjectsReturned:
        raise APIException(
            'There are more than one company with the provided slug.'
        )
    if not category.is_active:
        raise APIException(
            'The provided category has already been deactivated.'
        )
    category.is_active = ~F('is_active')
    category.save(update_fields=['is_active'])
