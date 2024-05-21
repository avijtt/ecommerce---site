from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import PaymentForm, ShippingForm
from django.contrib import messages

# Create your views here.
def payment_success(request):
	return render(request, "payment/payment_success.html", {})

def checkout(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods()
		quantities = cart.get_quants()
		totals = cart.cart_totals()
		
		if request.user.is_authenticated:
			# Checkout as logged in user
			# Shipping User
			shipping_user =ShippingAddress.objects.get(user__id = request.user.id)
			# Shipping Form
			shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
			return render(request, "payment/payment_checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
		else:
			# Checkout as guest
			shipping_form = ShippingForm(request.POST or None)
			return render(request, "payment/payment_checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

	else:
		messages.success(request, "Access Denied")
		return redirect("home")


def billing_info(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_totals()

		# Create a session with Shipping Info
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping

		# Check to see if user is logged in
		if request.user.is_authenticated:
			# Get The Billing Form
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

		else:
			# Not logged in
			# Get The Billing Form
			billing_form = PaymentForm()
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

		
	else:
		messages.success(request, "Access Denied")
		return redirect('home')