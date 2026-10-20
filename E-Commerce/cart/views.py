from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart

@login_required(login_url='users:login')
def cart_view(request):
    """
    Renders user shopping cart with item listing, live quantity modification, and order subtotal.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
    })
