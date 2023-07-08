from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from  .models import Gigs, User, Portfolio, Reviews, Business
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

class GigSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    class Meta:
        model = Gigs
        fields = ['gig_name', 'gig_description', 'gig_price', 'gig_negotiable', 'gig_location', 'gig_service_type', 'gig_image', 'service_provider']

class PortfolioSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = Portfolio
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = Business
        fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):
    gigs = GigSerializer(many=True, read_only=True)
    portfolio = PortfolioSerializer(many=True, read_only=True)
    business = BusinessSerializer(read_only = True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'email': {'read_only': True},
            'password': {'write_only': True}
        }



class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()

class PassVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_token = serializers.CharField()
    password = serializers.CharField()