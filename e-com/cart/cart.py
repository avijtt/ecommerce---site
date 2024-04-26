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

    def add(self, product):
        product_id = str(product.id)
        # check if product  already in cart
        # if product_id in self.cart:
        #     pass
        # else:
        #     self.cart[product_id]={'price' : product.price}

        self.session.modified = True
