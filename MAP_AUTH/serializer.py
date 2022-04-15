from rest_framework import serializers
from django.contrib.auth.models import User



class AuthRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['password']
        )
        return user

