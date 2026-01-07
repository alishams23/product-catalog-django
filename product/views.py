from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product, RootCategory
from .serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    RootCategoryListSerializer,
)


class ProductListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 60


class CategoryListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 60


class ProductListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductListSerializer
    pagination_class = ProductListPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ("title", "short_description", "description")
    ordering_fields = ("created_at", "title")
    ordering = ("-created_at",)

    def get_queryset(self):
        return (
            Product.objects.all()
            .order_by("-created_at")
            .distinct()
        )


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Product.objects.all()
            .distinct()
        )


class ProductCreateAPIView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductCreateSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        output = ProductDetailSerializer(product, context=self.get_serializer_context())
        return Response(output.data, status=status.HTTP_201_CREATED)


class CategoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryListSerializer
    pagination_class = CategoryListPagination

    def get_queryset(self):
        return Category.objects.select_related("root_category").order_by("name")


class CategoryDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.select_related("root_category")


class RootCategoryListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RootCategoryListSerializer

    def get_queryset(self):
        return RootCategory.objects.prefetch_related("categories").order_by("name")
