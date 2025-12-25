from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductFeature,
    ProductMedia,
    ProductSpecification,
    RootCategory,
)


class RootCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    root_category = RootCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "root_category")


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ("id", "media_type", "title", "url", "alt_text", "is_primary", "sort_order")


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ("id", "title", "body", "sort_order")


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ("id", "name", "value", "unit", "sort_order")


class ProductListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "primary_image",
            "categories",
            "is_featured",
            "published_at",
        )

    def get_primary_image(self, obj):
        media = next((item for item in obj.media.all() if item.is_primary), None)
        if media is None:
            media = obj.media.first()
        if not media:
            return None
        return {"url": media.url, "alt_text": media.alt_text}


class ProductDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "description",
            "highlights",
            "applications",
            "technical_overview",
            "model_number",
            "brand",
            "warranty",
            "datasheet_url",
            "brochure_url",
            "demo_video_url",
            "meta_title",
            "meta_description",
            "categories",
            "media",
            "features",
            "specifications",
            "is_featured",
            "published_at",
        )
