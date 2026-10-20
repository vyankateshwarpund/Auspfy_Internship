from django.urls import path
from orders.views import checkout_view, order_list_view, order_detail_view

app_name = 'orders'

urlpatterns = [
    path('', order_list_view, name='order_list'),
    path('checkout/', checkout_view, name='checkout'),
    path('<str:order_number>/', order_detail_view, name='order_detail'),
]
