from rest_framework import serializers
from account.models import User
from .models import Portfolio, Business

class PortfolioSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    serviceImage_url = serializers.ReadOnlyField()

    class Meta:
        model = Portfolio
        fields = '__all__'

    

class BusinessSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = Business
        fields = '__all__'