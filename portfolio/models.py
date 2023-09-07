from django.db import models
from account.models import User
from cloudinary.models import CloudinaryField
from gigs.models import BaseModel
# Create your models here.
class Portfolio(BaseModel):
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    service_title = models.CharField(max_length=100)
    service_overview = models.CharField(max_length=1000, null=True)
    service_image = CloudinaryField('service_image')
    # service_image = models.ImageField(upload_to=get_image_filename, default='default.png')
    created_at = models.DateTimeField(auto_now=True)


    @property
    def serviceImage_url(self):
        if self.service_image:
            return(
                f"https://res.cloudinary.com/dcgkw0wzb/{self.service_image}"
            )
        else:
            return ('https://res.cloudinary.com/dcgkw0wzb/image/upload/v1690449071/samples/two-ladies.jpg')
    def __str__(self):
        return self.service_title

class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Business_name = models.CharField(max_length=30, null=True)
    experience = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True)
    alt_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=20) #change this to use a choice field later