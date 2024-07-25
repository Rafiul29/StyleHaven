from .models import CartItem,Cart
from .views import _cart_id

def counter(request):
  cart_count=0
  if 'admin' in request.path:
    return {}
  else:
    try:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      if request.user.is_authenticated:
        cart_items=CartItem.objects.all().filter(user=request.user)
        print(cart_items)
      else:
        cart_items=CartItem.objects.all().filter(cart=cart)
      cart_count=cart_items.count()
    except Cart.DoesNotExist:
      cart_count=0

    return dict(cart_count=cart_count)
