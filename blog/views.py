from rest_framework import generics, permissions

from .models import Blog
from .serializers import BlogDetailSerializer, BlogListSerializer


class BlogListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BlogListSerializer

    def get_queryset(self):
        queryset = (
            Blog.objects.filter(is_published=True)
            .select_related("author")
            .prefetch_related("categories")
            .order_by("-published_at", "-created_at")
        )
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        return queryset


class BlogDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Blog.objects.filter(is_published=True)
            .select_related("author")
            .prefetch_related("categories")
        )
