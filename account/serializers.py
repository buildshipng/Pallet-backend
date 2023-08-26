from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from  .models import User
import random
from gigs.serializers import GigSerializer
from portfolio.serializers import BusinessSerializer, PortfolioSerializer
 


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
    gigs = GigSerializer(many=True, read_only=True)
    portfolio = PortfolioSerializer(many=True, read_only=True)
    business = BusinessSerializer(read_only = True)
    avatar_url = serializers.ReadOnlyField()
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        #fields = '__all__'
        exclude = [
            'password',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_staff']
        read_only_fields = ['email', 'full_name']

        # extra_kwargs = {
        #     'email': {'read_only': True},
        #     'password': {'write_only': True}
        # }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("avatar")

        return representation



class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()

class PassVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()
class PassResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()