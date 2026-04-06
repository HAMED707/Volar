# =============================================================================
# apps/products/models.py
#
# Models for the products app.
# Includes: Category, Product, ProductImage, Attribute, AttributeValue,
#           ProductVariant
# =============================================================================

from django.db import models


# -----------------------------------------------------------------------------
# Category
# -----------------------------------------------------------------------------

class Category(models.Model):
    name   = models.CharField(max_length=255)
    slug   = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# Product
# -----------------------------------------------------------------------------

class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
    )
    name        = models.CharField(max_length=255)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    base_price  = models.DecimalField(max_digits=10, decimal_places=2)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# Product Image
# -----------------------------------------------------------------------------

class ProductImage(models.Model):
    product    = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image      = models.ImageField(upload_to='products/')
    alt_text   = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"


# -----------------------------------------------------------------------------
# Attribute  (e.g. "Color", "Size")
# -----------------------------------------------------------------------------

class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# Attribute Value  (e.g. "Red", "XL")
# -----------------------------------------------------------------------------

class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='values',
    )
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# -----------------------------------------------------------------------------
# Product Variant
# Each variant is a unique combination of attribute values (e.g. Red + XL).
# Has its own SKU, stock count, and optional price override.
# -----------------------------------------------------------------------------

class ProductVariant(models.Model):
    product        = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
    )
    attributes     = models.ManyToManyField(AttributeValue)
    sku            = models.CharField(max_length=100, unique=True)
    price_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Leave blank to use the product base price.',
    )
    stock     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_price(self):
        return self.price_override if self.price_override else self.product.base_price

    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        attrs = ', '.join(str(a) for a in self.attributes.all())
        return f"{self.product.name} ({attrs})"