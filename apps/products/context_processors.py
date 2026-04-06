# =============================================================================
# apps/products/context_processors.py
#
# Injects nav_categories into every template context so the navbar
# always has the top-level categories available without repeating
# the query in every view.
# =============================================================================

from .models import Category


# -----------------------------------------------------------------------------
# Nav categories
# -----------------------------------------------------------------------------

def nav_categories(request):
    return {
        "nav_categories": Category.objects.filter(parent=None).order_by("name")
    }