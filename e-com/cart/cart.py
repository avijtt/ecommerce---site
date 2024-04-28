from store.models import Product
class Cart:
    def __init__(self, request):
        self.session = request.session
        # get currenrt session key if exist
        cart = self.session.get("session_key")
        # for new user , no session key ; create one
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}
        # make sure cart is availiable to all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # check if product  already in cart
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id]={'price' : str(product.price)}
             self.cart[product_id]= int(product_qty)
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get the products ids
        product_ids = self.cart.keys()
        # use ids to look product in db
        products = Product.objects.filter(id__in = product_ids)
        # return products 
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities