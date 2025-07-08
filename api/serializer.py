from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
   
    password2 = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', "password2"]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        
        email = validated_data['email'].lower()
        password = validated_data['password']
        password2 = validated_data.pop('password2')  
        
        user = User(
            username=validated_data['username'],
            email=email,
        )
        user.set_password(password)
        user.save()

        return user
