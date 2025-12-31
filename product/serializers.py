from rest_framework import serializers

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


class CategorySerializer(serializers.ModelSerializer):
    root_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "root_category")

    def get_root_category(self, obj):
        root = obj.root_category
        if not root:
            return None
        return {"id": root.id, "name": root.name, "slug": root.slug}


class RootCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug")


class RootCategoryListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug", "categories")


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = (
            "id",
            "media_type",
            "role",
            "title",
            "url",
            "alt_text",
            "is_primary",
            "sort_order",
        )


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ("id", "title", "body", "sort_order")


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ("id", "name", "value", "unit", "sort_order")


class ProductNavItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductNavItem
        fields = ("anchor_id", "label", "sort_order")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        anchor_id = data.get("anchor_id")
        if not anchor_id and instance.href:
            anchor_id = instance.href.lstrip("#")
        return {"id": anchor_id or "", "label": data.get("label") or ""}


class ProductContentBlockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductContentBlockItem
        fields = ("label", "value", "sort_order")


class ProductContentBlockSerializer(serializers.ModelSerializer):
    items = ProductContentBlockItemSerializer(many=True, read_only=True)
    media = serializers.SerializerMethodField()

    class Meta:
        model = ProductContentBlock
        fields = ("block_type", "title", "body", "items", "media", "sort_order")

    def get_media(self, obj):
        if not obj.media:
            return None
        return {"url": obj.media.url, "alt_text": obj.media.alt_text}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        block_type = data.get("block_type")
        media = data.get("media")
        items = data.get("items") or []
        text = data.get("body") or ""
        title = data.get("title") or ""
        block_type_map = {
            "text": ProductContentBlock.TYPE_PARAGRAPH,
            "html": ProductContentBlock.TYPE_PARAGRAPH,
            "table": ProductContentBlock.TYPE_LIST,
        }
        normalized_type = block_type_map.get(block_type, block_type)
        content = {"type": normalized_type}

        if normalized_type == ProductContentBlock.TYPE_HEADING:
            content["text"] = title or text
        elif normalized_type == ProductContentBlock.TYPE_PARAGRAPH:
            content["text"] = text
        elif normalized_type == ProductContentBlock.TYPE_LIST:
            content["items"] = [
                item.get("label") or item.get("value") or ""
                for item in items
                if item.get("label") or item.get("value")
            ]
        elif normalized_type in {ProductContentBlock.TYPE_IMAGE, ProductContentBlock.TYPE_VIDEO} and media:
            content["src"] = media.get("url")
            content["alt"] = media.get("alt_text") or ""

        return content


class ProductSpecItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecItem
        fields = ("name", "value", "unit", "sort_order")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"label": data.get("name") or "", "value": data.get("value") or ""}


class ProductSpecModelSerializer(serializers.ModelSerializer):
    specs = ProductSpecItemSerializer(source="spec_items", many=True, read_only=True)

    class Meta:
        model = ProductSpecModel
        fields = ("title", "specs", "sort_order")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"name": data.get("title") or "", "specs": data.get("specs") or []}


class ProductFaqItemSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(source="answer_html")

    class Meta:
        model = ProductFaqItem
        fields = ("question", "answer", "sort_order")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"question": data.get("question") or "", "answer": data.get("answer") or ""}


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
    class Meta:
        model = Product
        fields = ("slug",)

    def _primary_image(self, obj):
        media = next(
            (
                item
                for item in obj.media.all()
                if item.media_type == ProductMedia.TYPE_IMAGE and item.is_primary
            ),
            None,
        )
        if media is None:
            media = next(
                (
                    item
                    for item in obj.media.all()
                    if item.media_type == ProductMedia.TYPE_IMAGE
                ),
                None,
            )
        return media

    def _hero_image(self, obj):
        media = next(
            (
                item
                for item in obj.media.all()
                if item.media_type == ProductMedia.TYPE_IMAGE
                and item.role == ProductMedia.ROLE_HERO
            ),
            None,
        )
        return media or self._primary_image(obj)

    def _category_name(self, obj):
        category = obj.categories.first()
        return category.name if category else None

    def _category_href(self, obj):
        category = obj.categories.first()
        return f"/categories/{category.slug}" if category else None

    def _highlight(self, obj):
        return obj.highlight or obj.highlights or None

    def _highlight_html(self, obj):
        return obj.highlight_html or obj.highlights or None

    def _summary_html(self, obj):
        return obj.summary_html or obj.short_description or None

    def _hero_alt(self, obj, hero_media):
        if obj.hero_alt:
            return obj.hero_alt
        if hero_media:
            return hero_media.alt_text or None
        return None

    def _hero_title(self, obj):
        return obj.hero_title or obj.title

    def _hero_english(self, obj):
        return obj.hero_english or obj.title

    def _hero_video(self, obj):
        return obj.hero_video_url or obj.demo_video_url or None

    def _hero_catalog_href(self, obj):
        return obj.hero_catalog_href or obj.brochure_url or None

    def _hero_catalog_label(self, obj):
        if obj.hero_catalog_label:
            return obj.hero_catalog_label
        if obj.hero_catalog_href or obj.brochure_url:
            return "Catalog"
        return None

    def _spec_download_href(self, obj):
        return obj.spec_download_href or obj.datasheet_url or None

    def _blocks_by_section(self, obj, section):
        blocks = [block for block in obj.content_blocks.all() if block.section == section]
        return ProductContentBlockSerializer(blocks, many=True).data

    def _video_gallery(self, obj):
        videos = [
            item
            for item in obj.media.all()
            if item.media_type == ProductMedia.TYPE_VIDEO
            and item.role == ProductMedia.ROLE_GALLERY
        ]
        return [item.url for item in videos]

    def to_representation(self, instance):
        hero_media = self._hero_image(instance)
        image_media = self._primary_image(instance)
        nav_items = ProductNavItemSerializer(instance.nav_items.all(), many=True).data
        spec_models = ProductSpecModelSerializer(instance.spec_models.all(), many=True).data
        faq_items = ProductFaqItemSerializer(instance.faq_items.all(), many=True).data

        return {
            "slug": instance.slug,
            "title": instance.title,
            "image": image_media.url if image_media else None,
            "price": instance.price,
            "description": instance.description or None,
            "highlight": self._highlight(instance),
            "highlightHtml": self._highlight_html(instance),
            "summaryHtml": self._summary_html(instance),
            "category": self._category_name(instance),
            "categoryHref": self._category_href(instance),
            "cartHref": instance.cart_href or None,
            "heroImage": hero_media.url if hero_media else None,
            "heroAlt": self._hero_alt(instance, hero_media),
            "heroEnglish": self._hero_english(instance),
            "heroTitle": self._hero_title(instance),
            "heroTagline": instance.hero_tagline or None,
            "heroVideo": self._hero_video(instance),
            "heroCatalogHref": self._hero_catalog_href(instance),
            "heroCatalogLabel": self._hero_catalog_label(instance),
            "navItems": nav_items,
            "moarefiBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_MOAREFI),
            "moshakhasatBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_MOSHAKHASAT),
            "videoBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_VIDEO),
            "specModels": spec_models,
            "specDownloadHref": self._spec_download_href(instance),
            "videoGallery": self._video_gallery(instance),
            "faqItems": faq_items,
            "href": f"/products/{instance.slug}",
        }
