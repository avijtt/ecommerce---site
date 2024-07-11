from django.shortcuts import redirect, render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def cart_summery(request):
    cart = Cart(request)     # get the cart
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_totals() 
    context = {
        'cart_products':cart_products,
        'quantities' : quantities,
        'totals' : totals
    }
    return render(request, 'cart/cart_summery.html', context)


@login_required(login_url='login')  # Ensure the user is logged in
def cart_add(request):
    cart = Cart(request)  # Get the cart
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))  # Get product-id and quantity from jquery
        product_qty = int(request.POST.get('product_qty'))  # Lookup product
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, quantity=product_qty)  # Save the session
        cart_quantity = cart.__len__()  # Get cart Quantity

        response = JsonResponse({'Qty': cart_quantity})
        messages.success(request, 'Product Added to Cart')
        return response
    else:
        return redirect(reverse('login'))  # Redirect to login page if not authenticated

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
    #get from ajax
        product_id = int(request.POST.get('product_id'))
        cart.delete(product = product_id)
        response = JsonResponse({'product' : product_id})
        messages.success(request,'Product Removed from Cart')
        return response

    

def cart_update(request):
   cart = Cart(request)
   if request.POST.get('action') == 'post':
    #    get from ajax
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product = product_id, quantity = product_qty)
        response = JsonResponse({'qty' : product_qty})
        messages.success(request,'Product Updated from Cart')

        return response
        
