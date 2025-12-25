from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductFeature,
    ProductMedia,
    ProductSpecification,
    RootCategory,
)


@admin.register(RootCategory)
class RootCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "root_category", "created_at", "updated_at")
    list_filter = ("root_category",)
    search_fields = ("name", "slug", "root_category__name")
    prepopulated_fields = {"slug": ("name",)}


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 0
    fields = ("media_type", "title", "url", "alt_text", "is_primary", "sort_order")
    ordering = ("sort_order", "id")


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0
    fields = ("title", "body", "sort_order")
    ordering = ("sort_order", "id")


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 0
    fields = ("name", "value", "unit", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "is_featured",
        "published_at",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "is_featured", "categories", "created_at", "published_at")
    search_fields = (
        "title",
        "slug",
        "short_description",
        "description",
        "model_number",
        "brand",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = (
        ProductMediaInline,
        ProductFeatureInline,
        ProductSpecificationInline,
    )
    date_hierarchy = "published_at"


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("product", "media_type", "title", "is_primary", "sort_order")
    list_filter = ("media_type", "is_primary")
    search_fields = ("title", "alt_text", "url", "product__title")
    ordering = ("product", "sort_order", "id")


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ("product", "title", "sort_order", "created_at", "updated_at")
    search_fields = ("title", "body", "product__title")
    ordering = ("product", "sort_order", "id")


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "value", "unit", "sort_order")
    search_fields = ("name", "value", "unit", "product__title")
    ordering = ("product", "sort_order", "id")
