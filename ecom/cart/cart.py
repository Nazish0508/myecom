from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #get requests
        self.request = request

        #get session key if it exists
        cart = self.session.get('session_key')

        #if the user is new and doesn't have session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #login
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True 

        #deal with logged in request
        if self.request.user.is_authenticated:
            #get current profile user
            current_user = Profile.objects.filter(user__id = self.request.user.id)

            #convert ' to "
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")

            #save carty to the profile model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #login
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True 

        #deal with logged in request
        if self.request.user.is_authenticated:
            #get current profile user
            current_user = Profile.objects.filter(user__id = self.request.user.id)

            #convert ' to "
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")

            #save carty to the profile model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    
    def cart_totals(self):
        #get products ids
        product_ids = self.cart.keys()
        #lookup those keys in our products database model 
        products = Product.objects.filter(id__in = product_ids)
        #get quantities
        quantities = self.cart
        #start counting from 0
        total = 0
        for key, value in quantities.items():
            #convert key string into int
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total


    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

		# Get cart
        ourcart = self.cart
		# Update Dictionary/cart

        ourcart[product_id] = product_qty
        self.session.modified = True
    
        #deal with logged in request
        if self.request.user.is_authenticated:
            #get current profile user
            current_user = Profile.objects.filter(user__id = self.request.user.id)

            #convert ' to "
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")

            #save carty to the profile model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        #delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        #deal with logged in request
        if self.request.user.is_authenticated:
            #get current profile user
            current_user = Profile.objects.filter(user__id = self.request.user.id)

            #convert ' to "
            carty =str(self.cart)
            carty = carty.replace("\'", "\"")

            #save carty to the profile model
            current_user.update(old_cart=str(carty))

