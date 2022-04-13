from django.db import models
from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models



class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    class Meta:
        
        db_table = 'customer'

class CustomerParcel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
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




