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
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    highlight = models.CharField(max_length=240, blank=True)
    highlight_html = models.TextField(blank=True)
    summary_html = models.TextField(blank=True)
    hero_title = models.CharField(max_length=220, blank=True)
    hero_tagline = models.CharField(max_length=240, blank=True)
    hero_english = models.CharField(max_length=240, blank=True)
    hero_alt = models.CharField(max_length=200, blank=True)
    hero_video_url = models.URLField(blank=True)
    hero_catalog_href = models.URLField(blank=True)
    hero_catalog_label = models.CharField(max_length=200, blank=True)
    cart_href = models.URLField(blank=True)
    spec_download_href = models.URLField(blank=True)
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
    ROLE_HERO = "hero"
    ROLE_GALLERY = "gallery"
    ROLE_DOCUMENT = "document"
    TYPE_CHOICES = [
        (TYPE_IMAGE, "Image"),
        (TYPE_VIDEO, "Video"),
        (TYPE_DOCUMENT, "Document"),
    ]
    ROLE_CHOICES = [
        (ROLE_HERO, "Hero"),
        (ROLE_GALLERY, "Gallery"),
        (ROLE_DOCUMENT, "Document"),
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
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
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
            models.Index(fields=["product", "role"]),
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


class ProductNavItem(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="nav_items",
    )
    anchor_id = models.CharField(max_length=120, blank=True)
    label = models.CharField(max_length=120)
    href = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.label}"


class ProductContentBlock(AuditableModel):
    SECTION_MOAREFI = "moarefi"
    SECTION_MOSHAKHASAT = "moshakhasat"
    SECTION_VIDEO = "video"
    SECTION_CHOICES = [
        (SECTION_MOAREFI, "Moarefi"),
        (SECTION_MOSHAKHASAT, "Moshakhasat"),
        (SECTION_VIDEO, "Video"),
    ]
    TYPE_HEADING = "heading"
    TYPE_PARAGRAPH = "paragraph"
    TYPE_LIST = "list"
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_CHOICES = [
        (TYPE_HEADING, "Heading"),
        (TYPE_PARAGRAPH, "Paragraph"),
        (TYPE_LIST, "List"),
        (TYPE_IMAGE, "Image"),
        (TYPE_VIDEO, "Video"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="content_blocks",
    )
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    block_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    media = models.ForeignKey(
        ProductMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="content_blocks",
    )
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["product", "section"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.section} - {self.block_type}"


class ProductContentBlockItem(AuditableModel):
    block = models.ForeignKey(
        ProductContentBlock,
        on_delete=models.CASCADE,
        related_name="items",
    )
    label = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.block_id} - {self.label or self.value}"


class ProductSpecModel(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="spec_models",
    )
    title = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.title}"


class ProductSpecItem(AuditableModel):
    spec_model = models.ForeignKey(
        ProductSpecModel,
        on_delete=models.CASCADE,
        related_name="spec_items",
    )
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=300)
    unit = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.spec_model.title} - {self.name}"


class ProductFaqItem(AuditableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="faq_items",
    )
    question = models.CharField(max_length=240)
    answer_html = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.question}"
