from django.contrib import admin

from .models import (
    Furniture,
    Color,
    Company,
    Material,
    Category,
    FurnitureColor,
    FurnitureMaterial
)

admin.site.register(Furniture)
admin.site.register(Color)
admin.site.register(Company)
admin.site.register(Material)
admin.site.register(Category)
admin.site.register(FurnitureColor)
admin.site.register(FurnitureMaterial)
