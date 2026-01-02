from django.urls import path

from .views import (
    CategoryDetailAPIView,
    CategoryListAPIView,
    ProductCreateAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
    RootCategoryListAPIView,
)

app_name = "product"

urlpatterns = [
    path("root-categories/", RootCategoryListAPIView.as_view(), name="root-category-list"),
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("", ProductListAPIView.as_view(), name="product-list"),
    path("<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
