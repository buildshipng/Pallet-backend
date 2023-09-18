from django.db import models
from notification.models import Notifications
import uuid
from django.utils import timezone
from cloudinary.models import CloudinaryField

# Create your models here.]
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
class Gigs(BaseModel):
    service_provider = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='gigs')
    gig_name = models.CharField(max_length=100)
    gig_description = models.CharField(max_length=1000, null=True)
    gig_price = models.CharField(max_length=20, null=True)
    gig_negotiable = models.BooleanField("Negotiable", default=False)
    gig_location = models.CharField(max_length=20, null=True)
    gig_service_type = models.CharField(max_length=20, null=True)
    gig_image = CloudinaryField('gig_image')
    # gig_image = models.ImageField(upload_to=get_image_filename, default='default.png')

    @property
    def gigImage_url(self):
        if self.gig_image:
            return(
                f"https://res.cloudinary.com/dcgkw0wzb/{self.gig_image}"
            )
        else:
            return ('https://res.cloudinary.com/dcgkw0wzb/image/upload/v1690449071/samples/two-ladies.jpg')
    def __str__(self):
        return self.gig_name

class Reviews(models.Model):

    class CLOSE_GIG_CHOICE(models.TextChoices):
        """Documentation needed"""
        SERVICE_COMPLETED = 'service_completed', 'Service Completed'
        MIND_CHANGE = 'mind_change', 'Mind Change'
        SERVICE_PROVIDER_UNAVAILABLE = 'service_provider_unavailable', 'SERVICE PROVIDER UNAVAILABLE'
    # user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reviews')
    gig = models.ForeignKey(Gigs, on_delete=models.CASCADE, related_name='booked_gig')

    reviewer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reviewer')
    date_created = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0, blank=True)
    review_choice = models.CharField(max_length=255, choices=CLOSE_GIG_CHOICE.choices, blank=True)
    review_details = models.CharField(max_length=1000, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """Creating notfication for the gig's service provider"""
        super(Reviews, self).save(args, **kwargs)
        
        if self.review_choice == Reviews.CLOSE_GIG_CHOICE.SERVICE_COMPLETED:
            message = f'New review for your gig {self.gig.gig_name}'
        elif self.review_choice == Reviews.CLOSE_GIG_CHOICE.MIND_CHANGE:
            message = f'New review for your gig {self.gig.gig_name}'
        elif self.review_choice == Reviews.CLOSE_GIG_CHOICE.SERVICE_PROVIDER_UNAVAILABLE:
            message = f'New review for your gig {self.gig.gig_name}'
        else:
            Notifications.objects.create(client=self.reviewer, review=self.id, message=message)


class Bookings(BaseModel):
    gig = models.ForeignKey(Gigs, on_delete=models.CASCADE, related_name='booked_gigs')
    # booker = models.ForeignKey('account.user', on_delete=models.DO_NOTHING)
    #user booking the gig
    user = models.ForeignKey('account.user', on_delete=models.CASCADE)
    # status of the booking. Closed = 0 Open = 1
    status = models.BooleanField(default=False)