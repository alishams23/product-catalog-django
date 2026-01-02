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
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    title = models.CharField(max_length=220, help_text="Public product name.")
    slug = models.SlugField(max_length=240, unique=True, help_text="Used in product detail URL.")
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
        help_text="First category is used for category/categoryHref in the API.",
    )
    short_description = models.TextField(blank=True, help_text="Fallback for summaryHtml.")
    description = models.TextField(blank=True, default="", help_text="Full description content.")
    highlights = models.TextField(blank=True, help_text="Fallback for highlightHtml.")
    applications = models.TextField(blank=True, help_text="Legacy moarefi content.")
    technical_overview = models.TextField(blank=True, help_text="Legacy moshakhasat content.")
    model_number = models.CharField(max_length=120, blank=True, help_text="Internal model number.")
    brand = models.CharField(max_length=120, blank=True, help_text="Brand/manufacturer.")
    warranty = models.CharField(max_length=120, blank=True, help_text="Warranty label.")
    datasheet_url = models.FileField(
        upload_to="products/docs/",
        blank=True,
        help_text="Fallback for specDownloadHref.",
    )
    brochure_url = models.FileField(
        upload_to="products/docs/",
        blank=True,
        help_text="Fallback for heroCatalogHref.",
    )
    demo_video_url = models.FileField(
        upload_to="products/videos/",
        blank=True,
        help_text="Fallback for heroVideo.",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Displayed price.",
    )
    highlight = models.CharField(max_length=240, blank=True, help_text="Short highlight text.")
    highlight_html = models.TextField(blank=True, help_text="Rich highlight content.")
    summary_html = models.TextField(blank=True, help_text="Rich summary content.")
    hero_title = models.CharField(max_length=220, blank=True, help_text="Hero title text.")
    hero_tagline = models.CharField(max_length=240, blank=True, help_text="Hero tagline text.")
    hero_english = models.CharField(max_length=240, blank=True, help_text="Hero English text.")
    hero_alt = models.CharField(max_length=200, blank=True, help_text="Hero image alt text.")
    hero_video_url = models.FileField(
        upload_to="products/videos/",
        blank=True,
        help_text="Hero video file.",
    )
    hero_catalog_href = models.FileField(
        upload_to="products/docs/",
        blank=True,
        help_text="Hero catalog PDF.",
    )
    hero_catalog_label = models.CharField(
        max_length=200,
        blank=True,
        help_text="Label for the hero catalog link.",
    )
    cart_href = models.URLField(blank=True, help_text="Add-to-cart URL.")
    spec_download_href = models.FileField(
        upload_to="products/docs/",
        blank=True,
        help_text="Primary spec download file.",
    )
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title.")
    meta_description = models.TextField(blank=True, help_text="SEO description.")
    is_featured = models.BooleanField(default=False, help_text="Highlights product in lists.")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Controls ordering and publish time.",
    )

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
        help_text="Image, video, or document.",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        help_text="Hero vs gallery vs document.",
    )
    title = models.CharField(max_length=200, blank=True, help_text="Optional display title.")
    image = models.ImageField(
        upload_to="products/media/images/",
        null=True,
        blank=True,
        help_text="Required when media_type=image.",
    )
    file = models.FileField(
        upload_to="products/media/files/",
        null=True,
        blank=True,
        help_text="Required when media_type=video/document.",
    )
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for image/video.")
    is_primary = models.BooleanField(
        default=False,
        help_text="Used for list thumbnail when media_type=image.",
    )
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    title = models.CharField(max_length=200, help_text="Feature title.")
    body = models.TextField(blank=True, help_text="Feature body text.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    name = models.CharField(max_length=200, help_text="Specification name.")
    value = models.CharField(max_length=300, help_text="Specification value.")
    unit = models.CharField(max_length=50, blank=True, help_text="Optional unit.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    anchor_id = models.CharField(
        max_length=120,
        blank=True,
        help_text="Anchor id used by navItems.",
    )
    label = models.CharField(max_length=120, help_text="Visible nav label.")
    href = models.URLField(blank=True, help_text="Optional anchor href like #intro.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        help_text="Which section this block belongs to.",
    )
    block_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="Rendered block type.",
    )
    title = models.CharField(max_length=200, blank=True, help_text="Used by heading blocks.")
    body = models.TextField(blank=True, help_text="Paragraph or raw text content.")
    media = models.ForeignKey(
        ProductMedia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="content_blocks",
        help_text="Pick media for image/video blocks.",
    )
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    label = models.CharField(max_length=200, blank=True, help_text="List item label.")
    value = models.CharField(max_length=300, blank=True, help_text="List item value.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    title = models.CharField(max_length=200, help_text="Spec model title.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    name = models.CharField(max_length=200, help_text="Spec name.")
    value = models.CharField(max_length=300, help_text="Spec value.")
    unit = models.CharField(max_length=50, blank=True, help_text="Optional unit.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

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
    question = models.CharField(max_length=240, help_text="FAQ question.")
    answer_html = models.TextField(blank=True, help_text="FAQ answer HTML/text.")
    sort_order = models.PositiveIntegerField(default=0, help_text="Controls ordering.")

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"{self.product.title} - {self.question}"
