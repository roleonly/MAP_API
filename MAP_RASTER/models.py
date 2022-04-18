from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from MAP_PARCEL.models import Parcel

class raster_tiff(models.Model):   
    
    id = models.AutoField(primary_key=True)
    latitude= models.FloatField(default=0)
    longitude= models.FloatField(default=0)
    parcel=models.OneToOneField(Parcel, on_delete=models.CASCADE)
    URL = models.CharField(max_length=500) 
    elevation_max = models.FloatField(default=0)
    elevation_min = models.FloatField(default=0)
    width= models.FloatField(default=0)
    height= models.FloatField(default=0)
    scale= models.FloatField(default=0.00027777778)
              
    
   


    def __str__(self):
        return self.parcel

    class Meta:
        db_table = 'rastertiff'


class raster_image(models.Model):   
    
    id = models.AutoField(primary_key=True)
    URL = models.CharField(max_length=500) 
    xmlURL= models.CharField(max_length=500 ,default='')
    raster = models.ForeignKey(raster_tiff, on_delete=models.CASCADE, null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    color_range=models.CharField(max_length=1000, default='')            
   
    

    def __str__(self):
        return self.raster
    class Meta:
        db_table = 'rasterimage'




