from django.contrib import admin

from .forms import BlogAdminForm
from .models import Blog, Category, RootCategory


class CategoryInline(admin.TabularInline):
    model = Category
    fields = ("name", "slug")
    extra = 0
    show_change_link = True


@admin.register(RootCategory)
class RootCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CategoryInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "root_category", "created_at")
    list_filter = ("root_category",)
    search_fields = ("name", "slug", "root_category__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ("title", "is_published", "published_at", "created_at")
    list_filter = ("is_published", "categories", "categories__root_category")
    search_fields = ("title", "slug", "categories__name", "categories__root_category__name")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    filter_horizontal = ("categories",)
