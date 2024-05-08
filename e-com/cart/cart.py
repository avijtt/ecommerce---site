from store.models import Product,Profile
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("session_key")                                           # get currenrt session key if exist
        self.request = request                                                           # get request
        if "session_key" not in request.session:                                         # for new user , no session key ; create one
            cart = self.session["session_key"] = {}
        self.cart = cart                                                                # make sure cart is availiable to all pages

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:                                                      # check if product  already in cart
            pass
        else:
            self.cart[product_id]= int(product_qty)                                    # self.cart[product_id]={'price' : str(product.price)}
        self.session.modified = True

        if self.request.user.is_authenticated:                                          # for logged in user
            current_user = Profile.objects.filter(user__id = self.request.user.id)      # get current user profile
            carty = str(self.cart)                                                      # change dictionary to string
            carty  = carty.replace("\'", "\"")
            current_user.update(old_cart = str(carty))                                  # save carty to profile model

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()                                                  # get the products ids
        products = Product.objects.filter(id__in = product_ids)                         # use ids to look product in db
        return products                                                                 # return products 
   
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        ourcart = self.cart                                                              # get cart
        ourcart[product_id] = product_qty                                                # update dict
        self.session.modified = True
        
        
        if self.request.user.is_authenticated:                                          # for logged in user
            current_user = Profile.objects.filter(user__id = self.request.user.id)      # get current user profile
            carty = str(self.cart)                                                      # change dictionary to string
            carty  = carty.replace("\'", "\"")
            current_user.update(old_cart = str(carty))                                  # save carty to profile model
        thing = self.cart    
        return thing
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified=True
        
        if self.request.user.is_authenticated:                                          # for logged in user
            current_user = Profile.objects.filter(user__id = self.request.user.id)      # get current user profile
            carty = str(self.cart)                                                      # change dictionary to string
            carty  = carty.replace("\'", "\"")
            current_user.update(old_cart = str(carty))                                  # save carty to profile model

    def cart_totals(self):
        product_ids = self.cart.keys()                                                  # get product ids
        products = Product.objects.filter(id__in = product_ids)
        quantities = self.cart                                                          # get quantities
        total = 0
        for key,value in quantities.items():                                            # dictionary form as {'2' :4, '4' :3}
            key = int(key)
            value = int(value)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def cart_item(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:                                                      # check if product  already in cart
            pass
        else:
            self.cart[product_id]= int(product_qty)                                    # self.cart[product_id]={'price' : str(product.price)}
        self.session.modified = True

        if self.request.user.is_authenticated:                                          # for logged in user
            current_user = Profile.objects.filter(user__id = self.request.user.id)      # get current user profile
            carty = str(self.cart)                                                      # change dictionary to string
            carty  = carty.replace("\'", "\"")
            current_user.update(old_cart = str(carty))                                  # save carty to profile model

