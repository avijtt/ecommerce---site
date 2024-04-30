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
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # get cart
        ourcart = self.cart
        # update dict
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified=True

    def cart_totals(self):
        # get product isd
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        # get quantities
        quantities = self.cart
        total = 0
        # dictionary form as {'2' :4, '4' :3}
        for key,value in quantities.items():
            key = int(key)
            value = int(value)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
