# =============================================================================
# apps/products/views.py
#
# Views for the products app.
# Includes: ProductListView, ProductDetailView, CategoryView, SearchView
# =============================================================================

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Product


# -----------------------------------------------------------------------------
# Product List
# -----------------------------------------------------------------------------


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("images", "variants")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(parent=None)
        return context


# -----------------------------------------------------------------------------
# Product Detail
# -----------------------------------------------------------------------------


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("images", "variants__attributes__attribute")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Pass variants as JSON-friendly structure for HTMX / JS
        context["variants"] = product.variants.filter(is_active=True)
        context["primary_image"] = product.images.filter(is_primary=True).first()
        context["related_products"] = (
            Product.objects.filter(category=product.category, is_active=True)
            .exclude(pk=product.pk)
            .prefetch_related("images")[:4]
        )
        return context


# -----------------------------------------------------------------------------
# Category
# -----------------------------------------------------------------------------


class CategoryView(ListView):
    template_name = "products/category.html"
    context_object_name = "products"
    paginate_by = 12

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs["slug"])

    def get_queryset(self):
        category = self.get_category()

        # Include products from child categories too
        categories = [category] + list(category.children.all())

        return (
            Product.objects.filter(category__in=categories, is_active=True)
            .select_related("category")
            .prefetch_related("images", "variants")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        context["categories"] = Category.objects.filter(parent=None)
        return context


# -----------------------------------------------------------------------------
# Search
# -----------------------------------------------------------------------------


class SearchView(ListView):
    template_name = "products/search_results.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        if not query:
            return Product.objects.none()

        return (
            Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query),
                is_active=True,
            )
            .select_related("category")
            .prefetch_related("images", "variants")
            .distinct()
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        context["categories"] = Category.objects.filter(parent=None)
        return context