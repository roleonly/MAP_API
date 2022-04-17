
from MAP_PARCEL.views import ParcelView,CityView,CountryView,GeometryView,MapParcel
from django.urls import path



urlpatterns = [
     
    

    path('parcel/', ParcelView.as_view(), name='parcel'),
    path('city/', CityView.as_view(), name='city'),
    path('country/', CountryView.as_view(), name='country'),
    path('geometry/', GeometryView.as_view(), name='geometry'),
    path('map_parcel/', MapParcel.as_view(), name='map_parcel'),
]