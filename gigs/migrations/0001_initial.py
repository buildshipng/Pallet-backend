# Generated by Django 4.0.5 on 2023-07-31 14:42

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now=True)),
                ('rev_details', models.CharField(blank=True, max_length=600, null=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gigs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gig_name', models.CharField(max_length=100)),
                ('gig_description', models.CharField(max_length=1000, null=True)),
                ('gig_price', models.CharField(max_length=20, null=True)),
                ('gig_negotiable', models.BooleanField(default=False, verbose_name='Negotiable')),
                ('gig_location', models.CharField(max_length=20, null=True)),
                ('gig_service_type', models.CharField(max_length=20, null=True)),
                ('gig_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='gigImage')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gigs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]