# Generated by Django 4.0.4 on 2022-04-18 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAP_RASTER', '0007_raster_image_xmlurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='raster_image',
            name='color_range',
            field=models.CharField(default='', max_length=1000),
        ),
    ]