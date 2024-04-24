from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import SignUpForm

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


def product(request,pk):
	product = Product.objects.get(id = pk)
	context ={
	'product':product,
	}
	
	return render(request, 'store/product.html', context)