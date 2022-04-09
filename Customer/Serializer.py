from rest_framework import serializers
from django.contrib.auth.models import User
from Customer.models import *
class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        customer=Customer.objects.create(user=user,isActive=False,isDeleted=False)

        return user

class CustomerParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerParcel
        fields = ('id','name','owner','poly')