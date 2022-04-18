from turtle import color
from rest_framework import serializers

from MAP_PARCEL.models import Parcel
from MAP_PARCEL.serializer import ParcelSerializer
from MAP_RASTER.models import raster_tiff,raster_image

class RasterTiffSerializer(serializers.ModelSerializer):
    class Meta:
        model = raster_tiff
        fields = ('id', 'latitude', 'longitude', 'URL', 'elevation_max', 'elevation_min', 'width', 'height', 'scale')

class RasterPNGSerializer(serializers.ModelSerializer):
    class Meta:
        model = raster_image
        fields = ('id', 'URL','xmlURL','color_range')    