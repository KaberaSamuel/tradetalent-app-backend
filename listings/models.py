from django.db import models
from users.models import User
from django.utils.text import slugify


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, blank=True)
    type = models.CharField(max_length=200)
    work_mode  = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Listing.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)