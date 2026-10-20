from django.urls import path
from orders.api_views import OrderListCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='api-order-list-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='api-order-detail'),
]
