from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductContentBlock,
    ProductContentBlockItem,
    ProductFaqItem,
    ProductFeature,
    ProductMedia,
    ProductNavItem,
    ProductSpecItem,
    ProductSpecModel,
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
    fields = ("media_type", "role", "title", "url", "alt_text", "is_primary", "sort_order")
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


class ProductNavItemInline(admin.TabularInline):
    model = ProductNavItem
    extra = 0
    fields = ("anchor_id", "label", "href", "sort_order")
    ordering = ("sort_order", "id")


class ProductContentBlockInline(admin.TabularInline):
    model = ProductContentBlock
    extra = 0
    fields = ("section", "block_type", "title", "body", "media", "sort_order")
    ordering = ("sort_order", "id")


class ProductSpecModelInline(admin.TabularInline):
    model = ProductSpecModel
    extra = 0
    fields = ("title", "sort_order")
    ordering = ("sort_order", "id")


class ProductFaqItemInline(admin.TabularInline):
    model = ProductFaqItem
    extra = 0
    fields = ("question", "answer_html", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "is_featured",
        "price",
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
        "highlight",
        "hero_title",
        "model_number",
        "brand",
    )
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories",)
    inlines = (
        ProductMediaInline,
        ProductFeatureInline,
        ProductSpecificationInline,
        ProductNavItemInline,
        ProductContentBlockInline,
        ProductSpecModelInline,
        ProductFaqItemInline,
    )
    date_hierarchy = "published_at"


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("product", "media_type", "role", "title", "is_primary", "sort_order")
    list_filter = ("media_type", "role", "is_primary")
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


@admin.register(ProductNavItem)
class ProductNavItemAdmin(admin.ModelAdmin):
    list_display = ("product", "anchor_id", "label", "href", "sort_order")
    search_fields = ("anchor_id", "label", "href", "product__title")
    ordering = ("product", "sort_order", "id")


@admin.register(ProductContentBlock)
class ProductContentBlockAdmin(admin.ModelAdmin):
    list_display = ("product", "section", "block_type", "title", "sort_order")
    list_filter = ("section", "block_type")
    search_fields = ("title", "body", "product__title")
    ordering = ("product", "section", "sort_order", "id")


@admin.register(ProductContentBlockItem)
class ProductContentBlockItemAdmin(admin.ModelAdmin):
    list_display = ("block", "label", "value", "sort_order")
    search_fields = ("label", "value")
    ordering = ("block", "sort_order", "id")


@admin.register(ProductSpecModel)
class ProductSpecModelAdmin(admin.ModelAdmin):
    list_display = ("product", "title", "sort_order")
    search_fields = ("title", "product__title")
    ordering = ("product", "sort_order", "id")


@admin.register(ProductSpecItem)
class ProductSpecItemAdmin(admin.ModelAdmin):
    list_display = ("spec_model", "name", "value", "unit", "sort_order")
    search_fields = ("name", "value", "unit")
    ordering = ("spec_model", "sort_order", "id")


@admin.register(ProductFaqItem)
class ProductFaqItemAdmin(admin.ModelAdmin):
    list_display = ("product", "question", "sort_order")
    search_fields = ("question", "answer_html", "product__title")
    ordering = ("product", "sort_order", "id")
