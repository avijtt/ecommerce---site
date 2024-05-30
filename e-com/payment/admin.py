from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an orderitem inlines
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_order"]
    fields = ["user", "full_name", "email", "shipping_address", "amount", "date_order", "shipped"]
    inlines = [OrderItemInline]


# unregister User Model
admin.site.unregister(Order)

# reregister our order and orderItem
admin.site.register(Order, OrderAdmin)