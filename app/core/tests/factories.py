"""
Generating fake data for testing with factory boy module.
"""
import random
import factory
from faker import Faker
from django.utils.text import slugify
from django.utils import timezone

from store.models import (
    Furniture,
    Category,
    Company,
    Material,
    Color,
    FurnitureColor,
    FurnitureMaterial
)

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "%s" % (fake.name()))
    slug = slugify(name)
    description = fake.paragraph(nb_sentences=1)


class CompanyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Company

    name = factory.Sequence(lambda n: "%s" % (fake.name()))
    slug = slugify(name)
    ceo = fake.last_name()
    staff = fake.pyint()


class MaterialFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Material

    material = factory.Sequence(lambda n: "%s" % (fake.name()))
    slug = slugify(material)


class ColorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Color

    color = factory.Sequence(lambda n: "%s" % (fake.name()))
    slug = slugify(color)


class FurnitureFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Furniture

    name = factory.Sequence(lambda n: "%s" % (fake.name()))
    slug = slugify(name)
    price = 10.00
    stock = fake.pyint()
    rating = random.randint(1, 10)
    views = fake.pyint()
    image = fake.url()
    description = fake.paragraph(nb_sentences=1)
    category = factory.SubFactory(CategoryFactory)
    company = factory.SubFactory(CompanyFactory)
    produced_date = timezone.now()

    @factory.post_generation
    def color_furniture(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.color.add(**extracted)

    @factory.post_generation
    def material_furniture(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.color.add(**extracted)


class FurnitureMaterialFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = FurnitureMaterial

    furniture = factory.SubFactory(FurnitureFactory)
    material = factory.SubFactory(MaterialFactory)


class FurnitureColorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = FurnitureColor

    furniture = factory.SubFactory(FurnitureFactory)
    color = factory.SubFactory(ColorFactory)
