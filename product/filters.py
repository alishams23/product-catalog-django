import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="categories__slug", lookup_expr="iexact")
    category_id = django_filters.NumberFilter(field_name="categories__id")
    root_category = django_filters.CharFilter(
        field_name="categories__root_category__slug",
        lookup_expr="iexact",
    )
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ("category", "category_id", "root_category", "is_featured")
