from django.db import models
from uuid import uuid4

# Create your models here.
class Notifications(models.Model):
    """
    Notification model for service providers only.
        To be reviewed overtime
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    client = models.ForeignKey('account.user', on_delete=models.CASCADE, related_name="user", blank=False)
    
    # booking = models.ForeignKey('gigs.bookings', on_delete=models.CASCADE, related_name="client", blank=True,null=True)
    review = models.ForeignKey('gigs.reviews', on_delete=models.CASCADE,  related_name='client', blank=True, null=True)
    message = models.CharField(max_length=200, blank=False, null=False)
    notication_time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.message