from django.urls import path
from . import views

urlpatterns = [
    path("payment-success/", views.payment_success, name = "payment_success"),
     path("checkout/", views.checkout, name = "checkout"),
     path("billing-info/", views.billing_info, name = "billing_info"),
     path("process-order/", views.process_order ,name="process_order"),
     path("shipped-dash/", views.shipped_dash, name="shipped_dash"),
    path("not-shipped-dashdash/", views.not_shipped_dash, name="not_shipped_dash"),
    path("orders/<int:pk>/", views.orders, name="orders"),
]
   