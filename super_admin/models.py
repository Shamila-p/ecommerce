from email.mime import image
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField()
    

    @property
    def image_url(self):
        try:
            url=self.image.url
        except ValueError:
            url=""
        return url
