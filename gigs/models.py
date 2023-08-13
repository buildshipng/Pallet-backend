from django.db import models

from cloudinary.models import CloudinaryField

# Create your models here.
class Gigs(models.Model):
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
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reviewer')
    date_created = models.DateField(auto_now=True)
    rev_details = models.CharField(max_length=600, null=True, blank=True)