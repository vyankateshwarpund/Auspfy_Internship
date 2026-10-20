def cart_item_count(request):
    """
    Context processor to make current cart item count available across all templates.
    """
    count = 0
    if request.user.is_authenticated:
        try:
            from cart.models import Cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                count = sum(item.quantity for item in cart.items.all())
        except Exception:
            count = 0
    return {'cart_item_count': count}
