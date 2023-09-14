from django.db import models
from uuid import uuid4
from gigs.models import Bookings, Reviews


# Create your models here.
class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="user")
    booking_id = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name="client")
    review_id = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name="client_review")
    time_created = models.DateTimeField()
    message = models.CharField(max_length=100, blank=True)
    
    def __str__(self) -> str:
        return self.message