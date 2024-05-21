from django.urls import path
from . import views

urlpatterns = [
    path("payment-success/", views.payment_success, name = "payment_success"),
     path("checkout/", views.checkout, name = "checkout"),
     path("billing-info/", views.billing_info, name = "billing_info"),
]
   