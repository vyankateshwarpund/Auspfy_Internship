from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from orders.models import Order, OrderItem
from cart.models import Cart
from users.models import UserProfile

@login_required(login_url='users:login')
def checkout_view(request):
    """
    Renders checkout page, collects delivery address, validates inventory,
    creates the order within a transaction, reduces stock, and clears the user's cart.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = list(cart.items.select_related('product').all())

    if not items:
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('cart:cart_view')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')

        errors = []
        if not full_name:
            errors.append("Recipient full name is required.")
        if not email:
            errors.append("Email address is required.")
        if not phone_number:
            errors.append("Contact phone number is required.")
        if not shipping_address:
            errors.append("Delivery street address is required.")
        if not city:
            errors.append("City is required.")
        if not state:
            errors.append("State is required.")
        if not postal_code:
            errors.append("Postal code is required.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'items': items,
                'profile': profile,
            })

        # Atomic transaction to guarantee stock consistency
        with transaction.atomic():
            # 1. Stock check
            for item in items:
                if not item.product.is_active:
                    messages.error(request, f"Item '{item.product.name}' is no longer active.")
                    return redirect('cart:cart_view')
                if item.product.stock < item.quantity:
                    messages.error(
                        request,
                        f"Sorry, only {item.product.stock} units of '{item.product.name}' are available. Please update your cart."
                    )
                    return redirect('cart:cart_view')

            # 2. Server-calculated total
            total_amount = sum(Decimal(item.product.price) * item.quantity for item in items)

            # 3. Create Order
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                shipping_address=shipping_address,
                city=city,
                state=state,
                postal_code=postal_code,
                payment_method=payment_method,
                total_amount=total_amount,
                status=Order.STATUS_PENDING,
            )

            # 4. Create OrderItems & deduct stock
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock', 'updated_at'])

            # 5. Clear cart
            cart.items.all().delete()

        messages.success(request, f"Your order #{order.order_number} has been placed successfully!")
        return redirect('orders:order_detail', order_number=order.order_number)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'items': items,
        'profile': profile,
    })


@login_required(login_url='users:login')
def order_list_view(request):
    """
    Renders order history strictly for the authenticated user.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='users:login')
def order_detail_view(request, order_number):
    """
    Renders single order confirmation / invoice details strictly for the order owner.
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    items = order.items.all()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
    })
