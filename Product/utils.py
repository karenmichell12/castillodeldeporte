from .models import *
def get_or_create_cart(request):
    user = request.user if request.user.is_authenticated else None
    tienda_id = request.session.get('tienda_id')
    cart = pedido.objects.filter(tienda_id=tienda_id).first()

    if cart is None:
        cart= pedido.objects.create(user=user)
    
    if user and cart.user is None:
        cart.user = user
        cart.save()
    request.session['tienda_id']= cart.tienda_id

    return cart

def destroy_cart(request):
    request.session['tienda_id'] = None