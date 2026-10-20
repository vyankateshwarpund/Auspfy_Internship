from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart

class OrderListCreateAPIView(views.APIView):
    """
    GET /api/orders/ - List orders for the authenticated user
    POST /api/orders/ - Checkout and place an order from the user's cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response(
                {'error': 'Your cart is empty. Please add items before checking out.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = list(cart.items.select_related('product').all())

        # Atomic transaction to guarantee data integrity and safe stock deduction
        with transaction.atomic():
            # 1. Validate stock availability for all cart items first
            for item in cart_items:
                product = item.product
                if not product.is_active:
                    return Response(
                        {'error': f"Product '{product.name}' is no longer available."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if product.stock < item.quantity:
                    return Response(
                        {
                            'error': f"Insufficient stock for '{product.name}'. Requested: {item.quantity}, Available: {product.stock}."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 2. Compute total amount strictly on server
            total_amount = sum(Decimal(item.product.price) * item.quantity for item in cart_items)

            # 3. Create the Order
            data = serializer.validated_data
            order = Order.objects.create(
                user=request.user,
                full_name=data['full_name'],
                email=data['email'],
                phone_number=data['phone_number'],
                shipping_address=data['shipping_address'],
                city=data['city'],
                state=data['state'],
                postal_code=data['postal_code'],
                payment_method=data.get('payment_method', 'Cash on Delivery'),
                total_amount=total_amount,
                status=Order.STATUS_PENDING,
            )

            # 4. Create OrderItems & safely deduct stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                # Safely reduce stock
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock', 'updated_at'])

            # 5. Clear the user's cart
            cart.items.all().delete()

        return Response(
            {
                'message': 'Order placed successfully!',
                'order': OrderSerializer(order).data
            },
            status=status.HTTP_201_CREATED
        )


class OrderDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/orders/<id>/
    Retrieve order details strictly for the authenticated user who placed it.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')
