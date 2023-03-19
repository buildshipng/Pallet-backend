from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar', 'mobile', 'bio', 'location']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        data = super().validate(attrs)
        user = User.objects.get(email=data['email'])
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

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
        return user

class SettingsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar', 'mobile', 'bio', 'location']
        extra_kwargs = {'email': {'read_only': True}}