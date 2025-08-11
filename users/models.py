from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomUserManager

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=20)
    about = models.TextField()
    services_offered = models.CharField(max_length=200)
    services_needed = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()