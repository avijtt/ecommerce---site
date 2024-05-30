from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=100, )
    shipping_email = models.CharField(max_length=20)
    shipping_address1 = models.CharField(max_length=50)
    shipping_address2 = models.CharField(max_length=50, blank=True,null=True)
    shipping_city = models.CharField(max_length=30)
    shipping_state = models.CharField(max_length=30, blank=True,null=True)
    shipping_zipcode = models.CharField(max_length=10, blank=True,null=True)
    shipping_country = models.CharField(max_length=64)
    
    # dont pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}' 
    
# Create a user shipping Address  by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)


# order model
class Order(models.Model):
    # foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    shipping_address = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date_order = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Order - {str(self.id)}' 


# order items model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'Order Item - {str(self.id)}'

