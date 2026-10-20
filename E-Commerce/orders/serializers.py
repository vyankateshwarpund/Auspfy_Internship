from rest_framework import serializers
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'username',
            'full_name',
            'email',
            'phone_number',
            'shipping_address',
            'city',
            'state',
            'postal_code',
            'total_amount',
            'status',
            'payment_method',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['order_number', 'total_amount', 'status', 'created_at', 'updated_at']


class CheckoutSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    payment_method = serializers.CharField(max_length=50, default='Cash on Delivery', required=False)
