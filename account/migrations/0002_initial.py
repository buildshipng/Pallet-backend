# Generated by Django 4.0.5 on 2023-09-12 17:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0001_initial'),
        ('gigs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_gigs',
            field=models.ManyToManyField(blank=True, related_name='fav_gig', to='gigs.gigs'),
        ),
        migrations.AddField(
            model_name='user',
            name='fav_service',
            field=models.ManyToManyField(blank=True, related_name='fav_sp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
