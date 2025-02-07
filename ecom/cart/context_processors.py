from .cart import Cart

#create conrtext processor so out cart works on all pages
def cart(request):
    #return the default data from our cart
    return {'cart': Cart(request)}