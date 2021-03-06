from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from super_admin.models import Product
from datetime import datetime

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    profile_image = models.ImageField()

    @property
    def profile_image_url(self):
        try:
            url = self.profile_image.url
        except ValueError:
            url = ""
        return url


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price=models.IntegerField()
    address=models.TextField()
    ordered_date=models.DateTimeField(default=datetime.now())

