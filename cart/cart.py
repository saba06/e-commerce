from storefront.models import Product,Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        # get the current session key if it exist
        cart = self.session.get("session_key")

        # if user is new! No session_key create one!
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        
        # make sure cart is available on all pages of site
        self.cart=cart
    
    def db_add(self, product, quantity):
        
        product_id = str(product)
        product_qty = str(quantity)
        # is the product already in the cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)

        self.session.modified=True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # is the product already in the cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)

        self.session.modified=True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self,):
        return len(self.cart)
    
    def get_prods(self,):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities=self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id= str(product)
        quantity = int(quantity)
        self.cart[product_id]=quantity

        self.session.modified=True

        # if the user is logged in update to saved cart
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True

        # if the user is logged in  delete from saved cart
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(
                user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        return self.cart
    
    def get_total(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        return sum((product.sale_price if product.on_sale else product.price)*self.cart[str(product.id)] for product in products)