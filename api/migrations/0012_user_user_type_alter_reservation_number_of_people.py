# Generated by Django 5.1.7 on 2025-04-11 00:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('normal', 'Normal User'), ('owner', 'Owner')], default='normal', max_length=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='number_of_people',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
