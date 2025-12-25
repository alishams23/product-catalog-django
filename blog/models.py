from django.conf import settings
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


class Blog(AuditableModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    categories = models.ManyToManyField(
        Category,
        related_name="blogs",
        blank=True,
    )
    excerpt = models.TextField(blank=True)
    body = models.TextField(blank=True, default="")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_published", "published_at"]),
        ]

    def __str__(self) -> str:
        return self.title
