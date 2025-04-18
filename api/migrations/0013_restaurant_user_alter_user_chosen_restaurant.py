# Generated by Django 5.1.7 on 2025-04-11 21:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_restaurant_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='chosen_restaurant',
            field=models.ManyToManyField(related_name='related_rest+', through='api.Chosen', to='api.restaurant'),
        ),
    ]
