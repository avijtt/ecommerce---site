from .cart import Cart

# create contezt_processor so cart will work in all pages
def cart(request):
    # return the default data
    return {'cart'  : Cart(request)}