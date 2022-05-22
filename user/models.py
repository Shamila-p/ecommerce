from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone=models.CharField(max_length=15)
    profile_image=models.ImageField()
    @property
    def profile_image_url(self):
        try:
            url=self.profile_image.url
        except ValueError:
            url=""
        return url
