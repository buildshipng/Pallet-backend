# Generated by Django 4.0.5 on 2023-07-03 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_business_tokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokens',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
