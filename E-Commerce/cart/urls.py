from django.urls import path
from cart.views import cart_view

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart_view'),
]
