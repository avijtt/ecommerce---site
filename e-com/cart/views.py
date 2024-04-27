from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_summery(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    context = {
        'cart_products':cart_products
    }

    return render(request, 'cart/cart_summery.html', context)


def cart_add(request):
    # get the cart
    cart = Cart(request)
    # test for post
    if request.POST.get('action') == 'post':
        # get product-id from jquery
        product_id = int(request.POST.get('product_id'))     
        # lookup product
        product = get_object_or_404(Product, id = product_id)
        # save the session
        cart.add(product = product)
        
        # get cart Quantity
        cart_quantity = cart.__len__()

        # reurn response
        # response = JsonResponse({'product name': product.name})
        response = JsonResponse({' Qty': cart_quantity})
        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass

