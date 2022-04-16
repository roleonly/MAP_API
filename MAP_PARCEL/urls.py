
from MAP_PARCEL.views import ParcelView,CityView,CountryView
from django.urls import path



urlpatterns = [
     
    

    path('parcel/', ParcelView.as_view(), name='parcel'),
    path('city/', CityView.as_view(), name='city'),
    path('country/', CountryView.as_view(), name='country'),
]