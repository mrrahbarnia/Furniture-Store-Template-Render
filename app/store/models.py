"""
Tables for store app.
"""
import os
import uuid

from django.db import models
from django.urls import reverse
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

from common.models import BaseModel

def furniture_image_file_path(instance, filename):
    """Generating a file path for a new furniture image."""
    ext = os.path.splitext (filename)[1]
    unique_name = uuid.uuid4()
    filename = f'{unique_name}{ext}'

    path = os.path. join('uploads', 'furniture', filename)
    return path



class Furniture(BaseModel):
    """
    This class defines rows(attributes) of the Furniture table(class).
    """
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=160)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    ratings = models.PositiveIntegerField(
        validators=[
            MinValueValidator(limit_value=1), MaxValueValidator(limit_value=10)
        ]
    )
    views = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(
        upload_to=furniture_image_file_path, null=True, blank=True
    )
    description = models.TextField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, related_name='furniture'
    )
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True, related_name='furniture'
    )
    color = models.ManyToManyField(
        'Color', related_name='furniture', through='FurnitureColor'
    )
    material = models.ManyToManyField(
        'Material', related_name='furniture', through='FurnitureMaterial'
    )
    produced_date = models.DateField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("furniture_detail", args=[self.slug])


class Category(BaseModel):
    """
    This class defines rows(attributes) of the Category table(class).
    """
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=160)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", args=[self.slug])


class Company(BaseModel):
    """
    This class defines rows(attributes) of the Company table(class).
    """
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=160)
    ceo = models.CharField(max_length=100)
    staff = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", args=[self.slug])


class Material(BaseModel):
    """
    This class defines rows(attributes) of the Material table(class).
    """
    material = models.CharField(max_length=150)
    slug = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.material
    
    def get_absolute_url(self):
        return reverse("material_detail", args=[self.slug])
    

class Color(BaseModel):
    """
    This class defines rows(attributes) of the Color table(class).
    """
    color = models.CharField(max_length=150)
    slug = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.color
    
    def get_absolute_url(self):
        return reverse("material_detail", args=[self.slug])


class FurnitureMaterial(models.Model):
    """
    This class links the Furniture and 
    the Material models together(M2M link table).
    """
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE, related_name='furniture_fur_mat_link'
    )
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='material_fur_mat_link'
    )

    def __str__(self) -> str:
        return f'{self.furniture.name} >> {self.material.material}'


class FurnitureColor(models.Model):
    """
    This class links the Furniture and 
    the Color models together(M2M link table).
    """
    furniture = models.ForeignKey(
        Furniture, on_delete=models.CASCADE, related_name='furniture_fur_col_link'
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='color_fur_col_link'
    )

    def __str__(self) -> str:
        return f'{self.furniture.name} >> {self.color.color}'
