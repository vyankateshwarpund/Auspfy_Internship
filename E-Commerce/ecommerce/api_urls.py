from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('products.api_urls')),
    path('auth/', include('users.api_urls')),
    path('cart/', include('cart.api_urls')),
    path('orders/', include('orders.api_urls')),
]
