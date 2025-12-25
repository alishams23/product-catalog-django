from django.urls import path

from .views import ProductDetailAPIView, ProductListAPIView, RootCategoryListAPIView

app_name = "product"

urlpatterns = [
    path("root-categories/", RootCategoryListAPIView.as_view(), name="root-category-list"),
    path("", ProductListAPIView.as_view(), name="product-list"),
    path("<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
