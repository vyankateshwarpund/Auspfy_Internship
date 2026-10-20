from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cart.models import Cart, CartItem
from cart.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)

class CartAPIView(views.APIView):
    """
    GET /api/cart/
    Retrieve current authenticated user's cart with items and server-computed totals.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemAddAPIView(views.APIView):
    """
    POST /api/cart/items/
    Add a product to cart or increment quantity if already present.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return Response(
                    {'error': f"Cannot add {quantity} more. Only {product.stock} items in stock (you already have {cart_item.quantity} in cart)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        # Return updated cart
        return Response(
            {
                'message': f"Added '{product.name}' to cart successfully.",
                'cart': CartSerializer(cart).data,
                'cart_item': CartItemSerializer(cart_item).data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class CartItemDetailAPIView(views.APIView):
    """
    PATCH /api/cart/items/<id>/
    DELETE /api/cart/items/<id>/
    Update quantity or remove item from cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)

        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        desired_quantity = serializer.validated_data['quantity']
        if desired_quantity > cart_item.product.stock:
            return Response(
                {'error': f"Cannot set quantity to {desired_quantity}. Only {cart_item.product.stock} available in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = desired_quantity
        cart_item.save()

        return Response(
            {
                'message': 'Cart item quantity updated.',
                'cart': CartSerializer(cart).data,
                'cart_item': CartItemSerializer(cart_item).data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        product_name = cart_item.product.name
        cart_item.delete()

        return Response(
            {
                'message': f"'{product_name}' removed from your cart.",
                'cart': CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )
