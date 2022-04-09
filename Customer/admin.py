from django.contrib import admin

from django.contrib import admin
from django.db.models.base import ModelBase

from  Customer.models import Customer,CustomerParcel,Parcel

admin.site.register(Customer)
admin.site.register(CustomerParcel)
admin.site.register(Parcel)
