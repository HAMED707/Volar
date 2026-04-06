# =============================================================================
# apps/products/urls.py
#
# URL configuration for the products app.
# Routes: product list, product detail, category page, search results
# =============================================================================

from django.urls import path

from . import views

app_name = "products"

urlpatterns = [

    path("", views.ProductListView.as_view(), name="product_list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("category/<slug:slug>/", views.CategoryView.as_view(), name="category"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]