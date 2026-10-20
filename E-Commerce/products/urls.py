from django.urls import path
from products.views import home_view, product_list_view, product_detail_view

app_name = 'products'

urlpatterns = [
    path('', home_view, name='home'),
    path('products/', product_list_view, name='product_list'),
    path('category/<slug:category_slug>/', product_list_view, name='category_products'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
]
