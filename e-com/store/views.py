from django.shortcuts import render,redirect
from .models import Product, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import SignUpForm,UpdateUserForm

# Create your views here.
def home(request):
	products = Product.objects.all()
	context ={
		'products' : products
	}
	return render(request,'store/home.html',context)


def about(request):
	context = {}
	return render(request, 'store/about.html',context )


def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(request, username=username,password=password)
			login(request,user)
			messages.success(request,'Account has been created')
			return redirect('home')
		else:
			messages.success(request,'There seems to be problem')
			return redirect('register')
		
	else:	
		context = {'form':form}
		return render(request, 'register.html',context )


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password =request.POST['password']
		user =authenticate(request, username = username, password = password)
		if user is not None:
			login(request,user)
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
		context = {
			'user_form':user_form
		}
		if user_form.is_valid():
			user_form.save()
			login(request, current_user)
			messages.success(request, 'User has been updated')
			return redirect('home')
		return render(request, 'update_user.html', context)
	else:
		messages.success(request, ' You must been logged in to update')
		return redirect('update_user')

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