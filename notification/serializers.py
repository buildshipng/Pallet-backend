from gigs.models import Bookings, Reviews
from account.models import User
from rest_framework import serializers
from notification.models import Notifications
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil


class NotificationSerializer(serializers.ModelSerializer):
    notification_count = serializers.SerializerMethodField(read_only=True)
    notifications = serializers.SerializerMethodField(read_only=True)
    notification_time_display = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        models = User
        fields = '__all__'

    def get_notification_count(self, obj):
        """Return the total number of notification for the user"""
        user_id = obj.id
        return Notifications.objects.filter(user_id=user_id, is_read=False).count()
    
    def get_notifications(self, obj):
        """Return all notification to the authorise user"""
        user_id = obj.id
        notifications = Notifications.objects.filter(user_id = user_id)
        notification_data = NotificationDetailSerializer(notifications, many=True)
        return notification_data
    
    def get_notification_time_display(self, obj):
        """Notification time in real time format """
        
        now = timezone.now()
        delta = now - obj.notification_time
        
        if delta.total_seconds() < 60:
            return "now"
        elif delta.total_seconds() < 3600:
            minutes_ago = int(delta.total_seconds() / 60)
            return f"{minutes_ago} minute{'s' if minutes_ago > 1 else ''} ago"
        elif delta.total_seconds() < 86400:
            hours_ago = int(delta.total_seconds() / 3600)
            return f"{hours_ago} hour{'s' if hours_ago > 1 else ''} ago"
        elif delta.total_seconds() < 604800:
            days_ago = int(delta.total_seconds() / 86400)
            return f"{days_ago} day{'s' if days_ago > 1 else ''} ago"
        elif delta.total_seconds() < 2419200:
            weeks_ago = int(delta.total_seconds() / 604800)
            return f"{weeks_ago} week{'s' if weeks_ago > 1 else ''} ago"
        else:
            months_ago = int(delta.total_seconds() / 2419200)
            return f"{months_ago} month{'s' if months_ago > 1 else ''} ago"
        
    def to_representation(self, instance):
        """Return explicitly declare fields on on request"""
        
        data = super().to_representation(instance)
        data['notification_count'] = self.get_notification_count(instance)
        data['notifications'] = self.get_notifications(instance)
        data['notification_time_display'] = self.get_notification_time_display(instance)
        
        return data
    
class NotificationDetailSerializer(serializers.Serializer):
    class Meta:
        models = Notifications
        fields = "__all__"
        
    
        
    
        

    
    