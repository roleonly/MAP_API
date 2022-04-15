from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
# Create your models here.
class Parcel(models.Model):   
    
    ParcelType=((1,'City'),
                (2,'Country'),
                (3,'User')
                )
                
    owner = models.ManyToManyField(User, blank=True,related_name='parcels')
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=ParcelType, default=3)
    poly= models.MultiPolygonField(srid=4326)
    

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'parcel'