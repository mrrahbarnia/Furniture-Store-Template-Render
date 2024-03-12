"""
Tables for store app.
"""
import os
import uuid

from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

from common.models import BaseModel
from users.models import BaseUser


def furniture_image_file_path(instance, filename):
    """Generating a file path for a new furniture image."""
    ext = os.path.splitext(filename)[1]
    unique_name = uuid.uuid4()
    filename = f'{unique_name}{ext}'

    path = os.path. join('uploads', 'furniture', filename)
    return path


class Furniture(BaseModel):
    """
    This class defines rows(attributes) of the Furniture table(class).
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=160)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    ratings = models.ManyToManyField(
        'Rating', related_name='furniture_rating', through='FurnitureRating'
    )
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(
        upload_to=furniture_image_file_path, null=True, blank=True
    )
    description = models.TextField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL,
        null=True, related_name='furniture_category'
    )
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL,
        null=True, related_name='furniture_company'
    )
    color = models.ManyToManyField(
        'Color', related_name='furniture_color', through='FurnitureColor'
    )
    material = models.ManyToManyField(
        'Material', related_name='furniture_material',
        through='FurnitureMaterial'
    )
    produced_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("furniture_detail", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), name='unique_furniture_name'
            )
        ]


class Rating(BaseModel):
    """
    This class defines rows(attributes) of the Rating table(class).
    """
    """
    IF a user was deleted, his ratings for any furniture not delete at all.
    this logic used for statistics of the
    popularity of the specific furniture
    """
    user = models.ForeignKey(
        BaseUser, on_delete=models.SET_NULL, null=True, related_name='rating'
    )
    rating = models.SmallIntegerField(validators=[
            MinValueValidator(limit_value=0), MaxValueValidator(limit_value=10)
        ])

    def __str__(self) -> str:
        return f'{self.user} >> {self.rating}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name='check_rating_limitation',
                violation_error_message='Rating invalid...\
                    (Less than 10 and more than 0)'
            )
        ]


class Category(BaseModel):
    """
    This class defines rows(attributes) of the Category table(class).
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=160)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), name='unique_category'
            )
        ]


class Company(BaseModel):
    """
    This class defines rows(attributes) of the Company table(class).
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=160)
    ceo = models.CharField(max_length=100)
    staff = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), name='unique_company'
            )
        ]


class Material(BaseModel):
    """
    This class defines rows(attributes) of the Material table(class).
    """
    material = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.material

    def get_absolute_url(self):
        return reverse("material_detail", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('material').desc(), name='unique_material'
            )
        ]


class Color(BaseModel):
    """
    This class defines rows(attributes) of the Color table(class).
    """
    color = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.color

    def get_absolute_url(self):
        return reverse("material_detail", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('color'), name='unique_color'
            )
        ]


class FurnitureMaterial(models.Model):
    """
    This class links the Furniture and
    the Material models together(M2M link table).
    """
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE,
        related_name='furniture_fur_mat_link'
    )
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        related_name='material_fur_mat_link'
    )

    def __str__(self) -> str:
        return f'{self.furniture.name} >> {self.material.material}'

    class Meta:
        unique_together = ('furniture', 'material')


class FurnitureColor(models.Model):
    """
    This class links the Furniture and
    the Color models together(M2M link table).
    """
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE,
        related_name='furniture_fur_col_link'
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='color_fur_col_link'
    )

    def __str__(self) -> str:
        return f'{self.furniture.name} >> {self.color.color}'

    class Meta:
        unique_together = ('furniture', 'color')


class FurnitureRating(models.Model):
    """
    This class links the Furniture and
    the Rating models together(M2M link table).
    """
    furniture = models.ForeignKey(
        Furniture, on_delete=models.SET_NULL, null=True,
        related_name='furniture_fur_rat_link'
    )
    rating = models.ForeignKey(
        Rating, on_delete=models.SET_NULL, null=True,
        related_name='color_fur_col_link'
    )

    class Meta:
        unique_together = ('furniture', 'rating')

    def clean(self) -> None:
        """
        Every user can only rate a specific furniture one time not more.
        """
        qs = (Q(rating__user=self.rating.user) & Q(furniture=self.furniture))
        if FurnitureRating.objects.filter(qs).exists():
            raise ValidationError(
                'Only one rating must be exist for users and furniture.'
            )

    def __str__(self) -> str:
        return f'{self.rating} >> {self.furniture}'
