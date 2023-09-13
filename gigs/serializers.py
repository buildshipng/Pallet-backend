from rest_framework import serializers
from account.models import User
from .models import Gigs, Bookings
from django.db import models


class GigSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    gig_image = serializers.ImageField(required=False)
    class Meta:
        model = Gigs
        fields = '__all__'

class BookingSerializer(serializers.Serializer):
    gig_id = serializers.UUIDField()

class ClosingSerializer(serializers.Serializer):
    class CLOSE_GIG_CHOICE(models.TextChoices):
        SERVICE_COMPLETED = 'service_completed', 'Service Completed'
        MIND_CHANGE = 'mind_change', 'Mind Change'
        SERVICE_PROVIDER_UNAVAILABLE = 'service_provider_unavailable', 'SERVICE PROVIDER UNAVAILABLE'
    booking_id = serializers.UUIDField()
    review_choice = serializers.ChoiceField(choices=CLOSE_GIG_CHOICE.choices)
    rating = serializers.FloatField()
    review_experience = serializers.CharField(required=False)