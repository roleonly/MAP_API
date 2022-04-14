from django.db import models
from django.contrib.auth.models import User


class CustomerParcel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    poly= models.MultiPolygonField(srid=4326)
    
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'customerparcel'


#pre data customers can add to CustomerParcel
class Parcel(models.Model):   
    
    ParcelType=((1,'City'),
                (2,'Country'))

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=ParcelType, default=1)
    poly= models.MultiPolygonField(srid=4326)
    

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'parcel'




