"""
Custom command for creating fake data.
"""
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

from users.models import BaseUser
from store.models import (
    Furniture,
    Category,
    Company,
    Material,
    Color,
    Rating
)

User = settings.AUTH_USER_MODEL
fake = Faker()


class Command(BaseCommand):

    help = 'Generating fake data for models.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        for i in range(1, 51):

            try:
                category_name: str = fake.name()
                sample_category = Category.objects.create(
                    name=category_name,
                    slug=slugify(category_name),
                )

                company_name: str = fake.name()
                sample_company = Company.objects.create(
                    name=company_name,
                    slug=slugify(company_name),
                    ceo=fake.last_name(),
                    description=fake.paragraph(nb_sentences=1),
                    staff=fake.pyint()
                )

                material_name1: str = fake.name()
                sample_material1 = Material.objects.create(
                    material=material_name1,
                    slug=slugify(material_name1)
                )
                material_name2: str = fake.name()
                sample_material2 = Material.objects.create(
                    material=material_name2,
                    slug=slugify(material_name2)
                )

                color1: str = fake.color()
                sample_color1 = Color.objects.create(
                    color=color1, slug=slugify(color1)
                )
                color2: str = fake.color()
                sample_color2 = Color.objects.create(
                    color=color2, slug=slugify(color2)
                )

                sample_user1 = BaseUser.objects.create_user(
                    email=fake.email(), password='1234@example.com'
                )
                sample_user2 = BaseUser.objects.create_user(
                    email=fake.email(), password='1234@example.com'
                )
                sample_rating1 = Rating.objects.create(
                    user=sample_user1,
                    rating=fake.pyint(min_value=0, max_value=10)
                )
                sample_rating2 = Rating.objects.create(
                    user=sample_user2,
                    rating=fake.pyint(min_value=0, max_value=10)
                )

                furniture_name: str = fake.name()
                sample_furniture = Furniture.objects.create(
                    name=furniture_name,
                    slug=slugify(furniture_name),
                    price=10.00,
                    stock=fake.pyint(),
                    views=fake.pyint(),
                    image=fake.url(),
                    description=fake.paragraph(nb_sentences=1),
                    category=sample_category,
                    company=sample_company,
                    produced_date=timezone.now()
                )

                sample_furniture.color.add(sample_color1, sample_color2)
                sample_furniture.material.add(
                    sample_material1, sample_material2
                )
                sample_furniture.ratings.add(sample_rating1, sample_rating2)
                self.stdout.write(f'{i} object created...')
            except Exception:
                self.stdout.write(
                    self.style.ERROR(
                        f'Object number {i} has not been created.'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('Finished generating fake data.')
        )
