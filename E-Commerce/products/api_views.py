from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__slug")
    category_id = django_filters.NumberFilter(field_name="category__id")

    class Meta:
        model = Product
        fields = ['category', 'category_id', 'min_price', 'max_price']


class CategoryListAPIView(generics.ListAPIView):
    """
    GET /api/categories/
    List all categories with product counts.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    pagination_class = None


class ProductListAPIView(generics.ListAPIView):
    """
    GET /api/products/
    List active products with search, category filtering, price filtering, and sorting.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku', 'category__name']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/products/<id>/
    Retrieve detailed information for a single product.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
