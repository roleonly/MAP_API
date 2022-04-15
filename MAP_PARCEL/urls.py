
from MAP_PARCEL.views import ParcelView
from django.urls import path



urlpatterns = [
     
    

    path('parcel/', ParcelView.as_view(), name='parcel'),
    
]