# Generated by Django 4.0.4 on 2022-04-18 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MAP_RASTER', '0003_remove_raster_image_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raster_tiff',
            old_name='longtitude',
            new_name='longitude',
        ),
    ]
