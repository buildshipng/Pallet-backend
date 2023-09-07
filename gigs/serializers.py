from rest_framework import serializers
from account.models import User
from .models import Gigs, Bookings


class GigSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    gig_image = serializers.ImageField(required=False)
    class Meta:
        model = Gigs
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'