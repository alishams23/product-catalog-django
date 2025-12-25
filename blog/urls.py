from django.urls import path

from .views import BlogDetailAPIView, BlogListAPIView, RootCategoryListAPIView

app_name = "blog"

urlpatterns = [
    path("root-categories/", RootCategoryListAPIView.as_view(), name="root-category-list"),
    path("", BlogListAPIView.as_view(), name="blog-list"),
    path("<slug:slug>/", BlogDetailAPIView.as_view(), name="blog-detail"),
]
