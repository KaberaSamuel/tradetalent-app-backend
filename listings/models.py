from django.db import models
from users.models import User


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    work_mode  = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title