# Generated by Django 4.0.4 on 2022-04-18 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MAP_RASTER', '0004_rename_longtitude_raster_tiff_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raster_tiff',
            name='raster_image',
        ),
        migrations.AddField(
            model_name='raster_image',
            name='raster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MAP_RASTER.raster_tiff'),
        ),
    ]
