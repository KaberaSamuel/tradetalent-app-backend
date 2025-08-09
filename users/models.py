from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    about = models.TextField()
    services_offered = models.CharField(max_length=200)
    services_needed = models.CharField(max_length=200)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()