# Generated by Django 4.0.4 on 2022-04-14 20:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MAP_AUTH', '0002_parcel_delete_customerparcel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='owner',
            field=models.ManyToManyField(blank=True, related_name='parcels', to=settings.AUTH_USER_MODEL),
        ),
    ]
