# Generated by Django 5.0.2 on 2024-03-23 21:11

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='country',
            field=models.CharField(max_length=45, verbose_name='Страна'),
        ),
    ]
