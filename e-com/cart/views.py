from django.shortcuts import render,redirect

# Create your views here.
def cart_summery(request):
    return render(request, 'cart/cart_summery.html', {})


def cart_add(request):
    pass

def cart_delete(request):
    pass

def cart_update(request):
    pass

