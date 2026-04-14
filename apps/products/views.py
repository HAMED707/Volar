
"""
    
"""


from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name="products/product_list.html"
    context_object_name="products"


class ProductDetailView(DetailView):
    model = Product
    template_name="products/product_detail.html"
    context_object_name="product"

class SearchView(ListView):
    model=Product
    template_name="products/search_results.html"
    context_object_name="products"

    def get_queryset(self):
        
        query=self.request.GET.get("q")
        if not query:
            return Product.objects.none()
        return Product.objects.filter(name__icontains=query)