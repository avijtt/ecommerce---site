from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.models import Order, OrderItem, ShippingAddress
from payment.forms import PaymentForm, ShippingForm
from django.contrib import messages
from store.models import Profile, Product
import datetime

# Create your views here.
def payment_success(request):
	return render(request, "payment/payment_success.html", {})

def checkout(request):
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
	
def process_order(request):
	if request.POST:
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_totals()

		payment_form  = PaymentForm(request.POST or None)  		# get billing info from last page
		my_shipping = request.session.get("my_shipping") 		# get shipping session

		# gather order info
		full_name = my_shipping["shipping_full_name"]
		email = my_shipping["shipping_email"]

		# generate shipping address from session
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount = totals

		# order create
		if request.user.is_authenticated:  			# logged in
			user = request.user
			# create order and get order
			create_order = Order(user = user, full_name = full_name, email = email, shipping_address = shipping_address, amount = amount)
			create_order.save()
			order_id = create_order.pk

			# get product info with id and price
			for product in cart_products():
				product_id = product.pk
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price
				
				# get quantity
				for key, value in quantities().items():
					if int(key) == product.id:
						# create order items
						create_order_item = OrderItem(order_id = order_id, product_id = product_id, user = user, quantity = value, price = price)
						create_order_item.save()

			# delete cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# delete cart
					del request.session[key]
				
			# delete cart from old database
			current_user = Profile.objects.filter(user__id = request.user.id)
			# delete shopping cart from old database
			current_user.update(old_cart = "")


			messages.success(request, "Order Placed")
			return redirect("home")
		
		else: 			# not logged in
			# create order 
			create_order = Order(full_name = full_name, email = email, shipping_address = shipping_address, amount = amount)
			create_order.save()
			order_id = create_order.pk
			for product in cart_products():
				product_id = product.pk
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price
				
				# get quantity
				for key, value in quantities().items():
					if int(key) == product.id:
						# create order items
						create_order_item = OrderItem(order_id = order_id, product_id = product_id, quantity = value, price = price)
						create_order_item.save()

			# delete cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# delete cart
					del request.session[key]
			messages.success(request, "Order Placed")
			return redirect("home")

	else:
		messages.success(request, "Access Denied")
		return redirect("home")	
	
def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped = True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')
		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect("home")

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped = False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')
		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect("home")

def orders(request,pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# get order 
		order = Order.objects.get(id = pk)
		# get order items
		order_items = OrderItem.objects.filter(id = pk)
		if request.POST:
			status = request.POST['shipping_status']
			# check true or false 
			if status == 'true':
				order = Order.objects.filter(id = pk)
				now  = datetime.datetime.now()
				order.update(shipped = True, date_shipped = now)
			else:
				order = Order.objects.filter(id = pk)
				order.update(shipped = False)
			messages.success(request, "Shipping Status Success ")
			return redirect("home")
		return render(request, "payment/orders.html", {"order":order, "order_items":order_items})
		 
	else:
		messages.success(request, "Access Denied")
		return redirect("home")
	
def my_order(request):
    if request.user.is_authenticated:
        # Retrieve orders for the authenticated user
        orders = Order.objects.filter(user=request.user)
        return render(request, 'payment/my_order.html', {'orders': orders})
    else:
        messages.success(request, "You need to be logged in to view your orders.")
        return redirect('login')  # Redirect to the login page or any other appropriate page

