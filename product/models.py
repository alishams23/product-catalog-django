from django.db import models

from common.models import AuditableModel


class RootCategory(AuditableModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    image = models.ImageField(upload_to="products/root-categories/", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "root categories"

    def __str__(self) -> str:
        return self.name


class Category(AuditableModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    image = models.ImageField(upload_to="products/categories/", null=True, blank=True)
    short_description = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    root_category = models.ForeignKey(
        RootCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Product(AuditableModel):
    title = models.CharField(max_length=220, help_text="Public product name.")
    slug = models.SlugField(max_length=240, unique=True, help_text="Used in product detail URL.")
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
        help_text="Product categories.",
    )
    short_description = models.TextField(blank=True, help_text="Short summary.")
    description = models.TextField(
        blank=True,
        default="",
        help_text="Quill rich text content.",
    )
    hero_image = models.ImageField(
        upload_to="products/hero/",
        null=True,
        blank=True,
        help_text="Hero image (optional).",
    )
    hero_video = models.FileField(
        upload_to="products/hero/",
        null=True,
        blank=True,
        help_text="Hero video (optional).",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.title


class ProductGalleryImage(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(
        upload_to="products/gallery/",
        help_text="Gallery image.",
    )
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["product"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.id}"


class ProductFaqItem(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="faq_items",
    )
    question = models.CharField(max_length=240, help_text="FAQ question.")
    answer = models.TextField(blank=True, help_text="FAQ answer text/HTML.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.question}"
