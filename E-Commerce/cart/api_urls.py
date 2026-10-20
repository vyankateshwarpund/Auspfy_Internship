from django.urls import path
from cart.api_views import CartAPIView, CartItemAddAPIView, CartItemDetailAPIView

urlpatterns = [
    path('', CartAPIView.as_view(), name='api-cart-detail'),
    path('items/', CartItemAddAPIView.as_view(), name='api-cart-item-add'),
    path('items/<int:pk>/', CartItemDetailAPIView.as_view(), name='api-cart-item-detail'),
]
