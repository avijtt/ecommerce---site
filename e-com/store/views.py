from django.shortcuts import render,redirect
from .models import Product, Category,Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from.forms import SignUpForm,UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.
def home(request):
	products = Product.objects.all()
	context ={ 'products' : products  }
	return render(request,'store/home.html',context)

def about(request):
	context = {}
	return render(request, 'store/about.html',context )

 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Username Created - Please Fill Out Your User Info Below...")
                return redirect('update_info')
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('register')
        else:
            # Debugging: Print form errors to console or log them
            print(form.errors)
            messages.error(request, "Whoops! There was a problem registering, please try again...")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password =request.POST['password']
		user =authenticate(request, username = username, password = password)
		if user is not None:
			login(request,user)
			
			# retrive old_cart value form db
			current_user = Profile.objects.get(user__id = request.user.id)
			saved_cart = current_user.old_cart

			# convert db string value to dict
			if saved_cart:
				converted_cart = json.loads(saved_cart) # convert dict using json
				cart = Cart(request) # added loaded dict to session
				for key,value in converted_cart.items():
					cart.cart_item(product = key, quantity = value)

			messages.success(request,"You are now logged in.")
			return redirect('home')
		else:
			messages.error(request,"Username or Password is incorrect")
			return redirect('login')
	else:
 		return render(request, 'login.html', {} )

def logout_user(request):
	logout(request)
	messages.success(request,(" You have been LoggedOut"))
	return redirect('home')

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id = request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance = current_user )
		context = { 'user_form':user_form }
		if user_form.is_valid():
			user_form.save()
			login(request, current_user)
			messages.success(request, 'User has been updated')
			return redirect('home')
		return render(request, 'update_user.html', context)
	else:
		messages.success(request, ' You must been logged in to update')
		return redirect('update_user')

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def update_info(request):
	if request.user.is_authenticated:
		# get current profile and current shipping user
		current_profile = Profile.objects.get(user__id = request.user.id)
		shipping_user =ShippingAddress.objects.get(user__id = request.user.id)
		# get form to display in page
		form = UserInfoForm(request.POST or None, instance=current_profile)
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		if form.is_valid() or  shipping_form.is_valid():
			# save the new information 
			form.save()
			shipping_form.save()
			messages.success(request, 'Your info has been updated')
			return redirect('home')
		context = {'form' : form, 'shipping_form':shipping_form }
		return render(request, 'update_info.html', context)
	else:
		messages.success(request, 'You must be logged in')
		return redirect('login')

def product(request,pk):
	product = Product.objects.get(id = pk)
	context ={'product':product}
	return render(request, 'store/product.html', context)

def category_content(request,foo):
	# replace space with hyphen
	foo=foo.replace('-', ' ')
	try:
		# look for category
		categories = Category.objects.get(name = foo)
		products = Product.objects.filter(category  = categories)
		context = {'categories' : categories, 'products' : products}
		return render(request,'store/category.html', context) 
	except:
		messages.success(request,'Category does not exist!')
		return redirect('home')

def category_summary(request):
	categories = Category.objects.all()
	context = {
		'categories': categories 
	}
	return render(request, 'store/category_summary.html', context)

def search(request):
	# determine if search is filled
	if request.method == "POST":
		searched = request.POST["searched"]
		# quer dartabase
		searched = Product.objects.filter(Q(name__icontains =searched) | Q(description__icontains = searched))
		# check for null
		if not searched:
			messages.success(request,'not found for search products')
			return render(request, 'store/search.html', {})
		else:
			return render(request, 'store/search.html', {'searched':searched})
	else:	
		return render(request, 'store/search.html', {})