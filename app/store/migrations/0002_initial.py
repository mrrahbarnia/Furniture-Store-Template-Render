# Generated by Django 5.0.2 on 2024-05-16 15:51

import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='furniturerating',
            name='rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_fur_col_link', to='store.rating'),
        ),
        migrations.AddField(
            model_name='furniture',
            name='ratings',
            field=models.ManyToManyField(related_name='furniture_rating', through='store.FurnitureRating', to='store.rating'),
        ),
        migrations.AlterUniqueTogether(
            name='furniturecolor',
            unique_together={('furniture', 'color')},
        ),
        migrations.AlterUniqueTogether(
            name='furniturematerial',
            unique_together={('furniture', 'material')},
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 0), ('rating__lte', 10)), name='check_rating_limitation', violation_error_message='Rating invalid...                    (Less than 10 and more than 0)'),
        ),
        migrations.AlterUniqueTogether(
            name='furniturerating',
            unique_together={('furniture', 'rating')},
        ),
        migrations.AddConstraint(
            model_name='furniture',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='unique_furniture_name'),
        ),
    ]
