from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=100, )
    shipping_email = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=30)
    shipping_state = models.CharField(max_length=30, blank=True,null=True)
    shipping_zipcode = models.CharField(max_length=10, blank=True,null=True)
    shipping_country = models.CharField(max_length=64)
    
    # dont pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}' 