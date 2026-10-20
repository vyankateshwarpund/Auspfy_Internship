from django.urls import path
from products.api_views import CategoryListAPIView, ProductListAPIView, ProductDetailAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
]
