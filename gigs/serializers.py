from rest_framework import serializers
from account.models import User
from .models import Gigs


class GigSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    gigImage_url = serializers.ReadOnlyField()
    class Meta:
        model = Gigs
        fields = ['gig_name', 'gig_description', 'gig_price', 'gig_negotiable', 'gig_location', 'gig_service_type', 'gigImage_url','service_provider']

    