from rest_framework import serializers

from MAP_PARCEL.models import Parcel



class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ('id', 'name', 'type', 'poly', 'owner')
    
   