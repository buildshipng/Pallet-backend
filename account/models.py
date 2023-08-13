from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
from django.contrib.auth.hashers import make_password
from cloudinary.models import CloudinaryField
from gigs.models import Gigs


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):  
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

def get_image_filename(instance, filename):
    user_id = instance.id
    return f"contents/avatar/{user_id}/{filename}"

class User(AbstractUser):
    """
    The model class responsible for handling users
    """
    first_name = None
    last_name = None
    username = None
    full_name = models.CharField(max_length=50)
    email = models.EmailField(('email address'), unique=True)
    mobile = models.CharField(max_length=20, null=True)
    bio = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=50, null=True)
    avatar = CloudinaryField("avatar")
    fav_gigs = models.ManyToManyField(Gigs, related_name="fav_gig", blank=True)
    fav_service = models.ManyToManyField('self', related_name="fav_sp", blank=True)
    # portfolio = models.ManyToManyField('portfolio', related_name="portfolio")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    @property
    def avatar_url(self):
        if self.avatar:
            return(
                f"https://res.cloudinary.com/dcgkw0wzb/{self.avatar}"
            )
        else:
            return(
                'https://res.cloudinary.com/dcgkw0wzb/image/upload/v1690449075/cld-sample.jpg'
            )

    def __str__(self):
        return self.full_name


class Tokens(models.Model):
    email = models.EmailField('email address')
    action = models.CharField(max_length=20)
    token = models.CharField(max_length=10)
    exp_date = models.FloatField()
    date_used = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Hash the token before saving in the DB
        self.token = make_password(self.token)
        super().save(*args, **kwargs)

