# =============================================================================
# apps/products/admin.py
#
# Admin configuration for the products app.
# Registers: Category, Product, ProductImage, Attribute, AttributeValue,
#            ProductVariant
# =============================================================================

from django.contrib import admin

from .models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductVariant,
)


# -----------------------------------------------------------------------------
# Inlines
# -----------------------------------------------------------------------------


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# -----------------------------------------------------------------------------
# Category
# -----------------------------------------------------------------------------


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# -----------------------------------------------------------------------------
# Product
# -----------------------------------------------------------------------------


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "base_price", "is_active", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline]


# -----------------------------------------------------------------------------
# Attribute
# -----------------------------------------------------------------------------


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# -----------------------------------------------------------------------------
# Attribute Value
# -----------------------------------------------------------------------------


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value")
    list_filter = ("attribute",)