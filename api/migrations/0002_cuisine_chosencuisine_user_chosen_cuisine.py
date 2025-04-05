# Generated by Django 5.1.7 on 2025-04-01 00:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ChosenCuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='chosenCuisine', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cuisine')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='chosen_cuisine',
            field=models.ManyToManyField(through='api.ChosenCuisine', to='api.cuisine'),
        ),
    ]
