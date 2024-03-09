# Generated by Django 5.0.2 on 2024-03-09 09:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_furniture_category_alter_furniture_color_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='furniture',
            name='rating',
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='furniturecolor',
            unique_together={('furniture', 'color')},
        ),
        migrations.AlterUniqueTogether(
            name='furniturematerial',
            unique_together={('furniture', 'material')},
        ),
        migrations.CreateModel(
            name='FurnitureRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('furniture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='furniture_fur_rat_link', to='store.furniture')),
                ('rating', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_fur_col_link', to='store.rating')),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='rating',
            field=models.ManyToManyField(related_name='furniture_rating', through='store.FurnitureRating', to='store.rating'),
        ),
    ]