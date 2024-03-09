"""
Store app admin panel config.
"""
from django.contrib import admin

from .models import (
    Furniture,
    Color,
    Company,
    Material,
    Category,
    Rating,
    FurnitureColor,
    FurnitureMaterial,
    FurnitureRating
)

admin.site.register(Furniture)
admin.site.register(Color)
admin.site.register(Rating)
admin.site.register(Company)
admin.site.register(Material)
admin.site.register(Category)
admin.site.register(FurnitureColor)
admin.site.register(FurnitureMaterial)
admin.site.register(FurnitureRating)
