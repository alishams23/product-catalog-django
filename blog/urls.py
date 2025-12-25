from django.urls import path

from .views import BlogDetailAPIView, BlogListAPIView

app_name = "blog"

urlpatterns = [
    path("blogs/", BlogListAPIView.as_view(), name="blog-list"),
    path("blogs/<slug:slug>/", BlogDetailAPIView.as_view(), name="blog-detail"),
]
