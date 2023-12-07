from .models import *
from .utils import get_or_create_cart
def get_or_create_order(cart,request):
    cart= get_or_create_cart(request)
    order = Order.objects.filter(cart=cart).first()

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)

    request.session['order_id'] = order.order_id

    return order

def destroy_order(request):
    request.session['order_id'] = None
