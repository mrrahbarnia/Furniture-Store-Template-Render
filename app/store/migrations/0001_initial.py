# Generated by Django 5.0.2 on 2024-03-08 16:26

import django.core.validators
import django.db.models.deletion
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
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=160)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('color', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=160)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=160)),
                ('ceo', models.CharField(max_length=100)),
                ('staff', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('material', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=160)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=160)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('ratings', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1), django.core.validators.MaxValueValidator(limit_value=10)])),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.furniture_image_file_path)),
                ('description', models.TextField()),
                ('produced_date', models.DateField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture', to='store.category')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture', to='store.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FurnitureColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_fur_col_link', to='store.color')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture_fur_col_link', to='store.furniture')),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='color',
            field=models.ManyToManyField(related_name='furniture', through='store.FurnitureColor', to='store.color'),
        ),
        migrations.CreateModel(
            name='FurnitureMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furniture_fur_mat_link', to='store.furniture')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_fur_mat_link', to='store.material')),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='material',
            field=models.ManyToManyField(related_name='furniture', through='store.FurnitureMaterial', to='store.material'),
        ),
    ]
