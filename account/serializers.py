from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
import random
 


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'avatar', 'mobile', 'bio', 'location']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     user = self.user
    #     refresh = self.get_token(user)

    #     data['refresh'] = str(refresh)
    #     data['access'] = str(refresh.access_token)

    #     return data

class RegisterSerializer(serializers.ModelSerializer):
    # verification_token = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'mobile']
        extra_kwargs = {'password': {'write_only': True}}
        required_feilds = ['mobile']

    mobile = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = User(
          email=validated_data['email'],
          full_name=validated_data['full_name'],
          mobile=validated_data['mobile']
          )
        user.set_password(validated_data['password'])
        user.is_active = False  
        
    
        user.save()
        return user

class SettingsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        # fields = '__all__'
        extra_kwargs = {'email': {'read_only': True}}
        exclude = ['password', 'date_joined', 'user_permissions']

# class BusinessSerializer(serializers.ModelSerializer):



class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()

class PassVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()
    password = serializers.CharField()