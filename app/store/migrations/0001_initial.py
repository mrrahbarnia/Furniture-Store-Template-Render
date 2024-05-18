# Generated by Django 5.0.2 on 2024-05-16 15:51

import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=160)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('color', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=160)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=160)),
                ('ceo', models.CharField(max_length=100)),
                ('staff', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=160)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.furniture_image_file_path)),
                ('description', models.TextField()),
                ('produced_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FurnitureRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('material', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=160)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=10)])),
            ],
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='unique_category'),
        ),
        migrations.AddConstraint(
            model_name='color',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('color'), name='unique_color'),
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='unique_company'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture_category', to='store.category'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture_company', to='store.company'),
        ),
        migrations.AddField(
            model_name='furniturecolor',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_fur_col_link', to='store.color'),
        ),
        migrations.AddField(
            model_name='furniturecolor',
            name='furniture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture_fur_col_link', to='store.furniture'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='color',
            field=models.ManyToManyField(related_name='furniture_color', through='store.FurnitureColor', to='store.color'),
        ),
        migrations.AddField(
            model_name='furniturematerial',
            name='furniture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture_fur_mat_link', to='store.furniture'),
        ),
        migrations.AddField(
            model_name='furniturerating',
            name='furniture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture_fur_rat_link', to='store.furniture'),
        ),
        migrations.AddConstraint(
            model_name='material',
            constraint=models.UniqueConstraint(models.OrderBy(django.db.models.functions.text.Lower('material'), descending=True), name='unique_material'),
        ),
        migrations.AddField(
            model_name='furniturematerial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_fur_mat_link', to='store.material'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='material',
            field=models.ManyToManyField(related_name='furniture_material', through='store.FurnitureMaterial', to='store.material'),
        ),
    ]
