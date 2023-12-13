# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.Filterset):#This is utilized for the search functionality
    name= django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'subcategory', 'image']
        