"""
Database layer for executing some operations on data.
"""
from django.db import transaction
from django.db.models import F

from store.models import Furniture, Rating, FurnitureRating
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
def rate_furniture(*, user:BaseUser, rate:int, slug:str):
    """
    This business logic execute three queries:
    1 => Create and returning a rating object.
    2 => Getting a specific furniture with a given slug.
    3 => Assign that rating to a specific furniture.
    """
    rating: Rating = Rating.objects.create(user=user, rating=rate)
    furniture = Furniture.objects.get(slug=slug)
    furniture_rate = FurnitureRating(rating=rating, furniture=furniture)
    furniture_rate.full_clean()
    furniture_rate.save()
