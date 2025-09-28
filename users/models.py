from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomUserManager
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100, default="")
    slug = AutoSlugField(populate_from="name", unique=True)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100, default="")
    about = models.TextField(default="")
    services_offered = models.CharField(max_length=200, default="")
    services_needed = models.CharField(max_length=200, default="")
    profile_image = CloudinaryField("image", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
