from django.db import models
import datetime

# Create your models here.
class Category(models.Model):
	name= models.CharField(max_length=100)

	def  __str__(self):
		return self.name
	
	class Meta:
		verbose_name = 'Categories'  #change the class name to Categories




class Customer(models.Model):
	first_name = models.CharField(max_length=50) 
	last_name = models.CharField(max_length=20)
	phone =  models.CharField(max_length=13)
	email =  models.EmailField(max_length=15)
	password = models.CharField(max_length=25)

	def  __str__(self):
		return f"{self.first_name} {self.last_name}"



class Product(models.Model):
	name = models.CharField(max_length=100) 
	price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.TextField(max_length=1000, default='', blank=True)
	image = models.ImageField(upload_to='upload/products/')
	# Add sales 
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=7)

	def   __str__(self):
		return self.name



class Order(models.Model):
	product = models.ForeignKey(Product, on_delete= models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity =  models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True )
	phone = models.CharField(max_length=10, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self) -> str:
		return self.product
	
