from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import PageNumberPagination

from .filters import ProductFilter
from .models import Product, RootCategory
from .serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
    RootCategoryListSerializer,
)


class ProductListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 60


class ProductListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductListSerializer
    pagination_class = ProductListPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ("title", "short_description", "description", "brand", "model_number")
    ordering_fields = ("published_at", "created_at", "title")
    ordering = ("-published_at", "-created_at")

    def get_queryset(self):
        return (
            Product.objects.filter(status=Product.STATUS_PUBLISHED)
            .prefetch_related("categories", "media")
            .order_by("-published_at", "-created_at")
            .distinct()
        )


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Product.objects.filter(status=Product.STATUS_PUBLISHED)
            .prefetch_related(
                "categories",
                "media",
                "features",
                "specifications",
                "nav_items",
                "content_blocks__items",
                "content_blocks__media",
                "spec_models__spec_items",
                "faq_items",
            )
            .distinct()
        )


class RootCategoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RootCategoryListSerializer

    def get_queryset(self):
        return RootCategory.objects.prefetch_related("categories").order_by("name")
