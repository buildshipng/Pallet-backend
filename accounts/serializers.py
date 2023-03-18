from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar', 'mobile', 'bio', 'location']
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
          email=validated_data['email'],
          full_name=validated_data['full_name'],
          )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class SettingsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar', 'mobile', 'bio', 'location']
        extra_kwargs = {'email': {'read_only': True}}