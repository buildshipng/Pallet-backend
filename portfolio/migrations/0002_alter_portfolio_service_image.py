# Generated by Django 4.0.5 on 2023-08-01 11:19

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='service_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='service_image'),
        ),
    ]
