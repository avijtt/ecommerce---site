from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_summery(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    context = {
        'cart_products':cart_products,
        'quantities' : quantities
    }
    return render(request, 'cart/cart_summery.html', context)


def cart_add(request):
    # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':
        # get product-id and quantity from jquery
        product_id = int(request.POST.get('product_id'))    
        product_qty =  int(request.POST.get('product_qty'))    
        # lookup product
        product = get_object_or_404(Product, id = product_id)
        # save the session
        cart.add(product = product, quantity = product_qty)
        
        # get cart Quantity
        cart_quantity = cart.__len__()

        # reurn response
        # response = JsonResponse({'product name': product.name})
        response = JsonResponse({' Qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
    #get from ajax
        product_id = int(request.POST.get('product_id'))
        cart.delete(product = product_id)
        response = JsonResponse({'product' : product_id})
        return response

    

def cart_update(request):
   cart = Cart(request)
   if request.POST.get('action') == 'post':
    #    get fro ajax
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product = product_id, quantity = product_qty)
        response = JsonResponse({'qty' : product_qty})
        return response
        
