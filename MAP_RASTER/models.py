from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from MAP_PARCEL.models import Parcel

class raster_tiff(models.Model):   
    
    id = models.AutoField(primary_key=True)
    parcel=models.ForeignKey(Parcel, on_delete=models.CASCADE)
    URL = models.CharField(max_length=500) 
    elevation_max = models.FloatField(default=0)
    elevation_min = models.FloatField(default=0)
    width= models.FloatField(default=0)
    height= models.FloatField(default=0)

                
   
    

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'rastertiff'


class raster_image(models.Model):   
    
    id = models.AutoField(primary_key=True)
    URL = models.CharField(max_length=500) 
    raster=models.ForeignKey(raster_tiff, on_delete=models.CASCADE)
                
   
    

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'rasterimage'