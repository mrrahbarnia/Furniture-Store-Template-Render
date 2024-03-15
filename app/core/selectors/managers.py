"""
Custom managers.
"""
from typing import override
from django.db import models
from django.db.models import QuerySet


class IsActiveManager(models.Manager):
    """
    Custom manager for only selecting active objects from models...
    This manager created for preventing repetitive codes.
    """
    @override
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)
