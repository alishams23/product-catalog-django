from django.db import models

from common.models import AuditableModel


class RootCategory(AuditableModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "root categories"

    def __str__(self) -> str:
        return self.name


class Category(AuditableModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
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
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
    )
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True, default="")
    highlights = models.TextField(blank=True)
    applications = models.TextField(blank=True)
    technical_overview = models.TextField(blank=True)
    model_number = models.CharField(max_length=120, blank=True)
    brand = models.CharField(max_length=120, blank=True)
    warranty = models.CharField(max_length=120, blank=True)
    datasheet_url = models.URLField(blank=True)
    brochure_url = models.URLField(blank=True)
    demo_video_url = models.URLField(blank=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "published_at"]),
        ]

    def __str__(self) -> str:
        return self.title


class ProductMedia(AuditableModel):
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_DOCUMENT = "document"
    TYPE_CHOICES = [
        (TYPE_IMAGE, "Image"),
        (TYPE_VIDEO, "Video"),
        (TYPE_DOCUMENT, "Document"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="media",
    )
    media_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_IMAGE,
    )
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField()
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["product", "media_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.media_type}"


class ProductFeature(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features",
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.title}"


class ProductSpecification(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
    )
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=300)
    unit = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.name}"
