from django.contrib import admin

from .forms import CategoryAdminForm, ProductAdminForm
from .models import (
    Category,
    Product,
    ProductGalleryImage,
    RootCategory,
)


@admin.register(RootCategory)
class RootCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ("name", "slug", "root_category", "created_at", "updated_at")
    list_filter = ("root_category",)
    search_fields = ("name", "slug", "root_category__name")
    prepopulated_fields = {"slug": ("name",)}


class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 0
    fields = ("image", "alt_text", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        "title",
        "created_at",
        "updated_at",
    )
    list_filter = ("categories", "created_at")
    search_fields = (
        "title",
        "slug",
        "short_description",
        "description",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = (
        ProductGalleryImageInline,
    )


@admin.register(ProductGalleryImage)
class ProductGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text", "sort_order")
    search_fields = ("alt_text", "product__title")
    ordering = ("product", "sort_order", "id")
