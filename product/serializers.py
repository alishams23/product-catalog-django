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


class CategoryListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="name")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("title", "image")

    def get_image(self, obj):
        if not obj.image:
            return None
        return self._build_absolute_url(obj.image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class CategoryDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="name")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "title", "slug", "image", "short_description", "description")

    def get_image(self, obj):
        if not obj.image:
            return None
        return self._build_absolute_url(obj.image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


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
    url = serializers.SerializerMethodField()

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

    def get_url(self, obj):
        if obj.media_type == ProductMedia.TYPE_IMAGE and obj.image:
            return self._build_absolute_url(obj.image.url)
        if obj.media_type in {ProductMedia.TYPE_VIDEO, ProductMedia.TYPE_DOCUMENT} and obj.file:
            return self._build_absolute_url(obj.file.url)
        return None

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


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
        media = obj.media
        if media.media_type == ProductMedia.TYPE_IMAGE and media.image:
            url = self._build_absolute_url(media.image.url)
        elif media.media_type in {ProductMedia.TYPE_VIDEO, ProductMedia.TYPE_DOCUMENT} and media.file:
            url = self._build_absolute_url(media.file.url)
        else:
            url = None
        return {"url": url, "alt_text": media.alt_text}

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path

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


class ProductNavItemOutputSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True, required=False)
    label = serializers.CharField(allow_blank=True, required=False)


class ContentBlockOutputSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=(
            ProductContentBlock.TYPE_HEADING,
            ProductContentBlock.TYPE_PARAGRAPH,
            ProductContentBlock.TYPE_LIST,
            ProductContentBlock.TYPE_IMAGE,
            ProductContentBlock.TYPE_VIDEO,
        )
    )
    text = serializers.CharField(allow_blank=True, required=False)
    items = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
    )
    src = serializers.CharField(allow_blank=True, required=False)
    alt = serializers.CharField(allow_blank=True, required=False)


class SpecItemOutputSerializer(serializers.Serializer):
    label = serializers.CharField(allow_blank=True, required=False)
    value = serializers.CharField(allow_blank=True, required=False)


class SpecModelOutputSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, required=False)
    specs = SpecItemOutputSerializer(many=True)


class FaqItemOutputSerializer(serializers.Serializer):
    question = serializers.CharField(allow_blank=True, required=False)
    answer = serializers.CharField(allow_blank=True, required=False)


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


class ProductMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = (
            "media_type",
            "role",
            "title",
            "image",
            "file",
            "alt_text",
            "is_primary",
            "sort_order",
        )

    def validate(self, attrs):
        media_type = attrs.get("media_type")
        image = attrs.get("image")
        file = attrs.get("file")
        if media_type == ProductMedia.TYPE_IMAGE and not image:
            raise serializers.ValidationError("image is required for image media.")
        if media_type in {ProductMedia.TYPE_VIDEO, ProductMedia.TYPE_DOCUMENT} and not file:
            raise serializers.ValidationError("file is required for video/document media.")
        return attrs


class ProductFeatureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ("title", "body", "sort_order")


class ProductSpecificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ("name", "value", "unit", "sort_order")


class ProductNavItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductNavItem
        fields = ("anchor_id", "label", "href", "sort_order")


class ProductContentBlockItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductContentBlockItem
        fields = ("label", "value", "sort_order")


class ProductContentBlockCreateSerializer(serializers.ModelSerializer):
    items = ProductContentBlockItemCreateSerializer(many=True, required=False)
    media = ProductMediaCreateSerializer(required=False)

    class Meta:
        model = ProductContentBlock
        fields = ("section", "block_type", "title", "body", "media", "items", "sort_order")


class ProductSpecItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecItem
        fields = ("name", "value", "unit", "sort_order")


class ProductSpecModelCreateSerializer(serializers.ModelSerializer):
    spec_items = ProductSpecItemCreateSerializer(many=True, required=False)

    class Meta:
        model = ProductSpecModel
        fields = ("title", "spec_items", "sort_order")


class ProductFaqItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFaqItem
        fields = ("question", "answer_html", "sort_order")


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
        if not media:
            return None
        url = media.image.url if media.image else None
        return {"url": self._build_absolute_url(url), "alt_text": media.alt_text}

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class ProductDetailSerializer(serializers.Serializer):
    slug = serializers.CharField()
    title = serializers.CharField()
    image = serializers.CharField(allow_null=True, required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    highlight = serializers.CharField(allow_blank=True, required=False)
    highlightHtml = serializers.CharField(allow_blank=True, required=False)
    summaryHtml = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField(allow_blank=True, required=False)
    categoryHref = serializers.CharField(allow_blank=True, required=False)
    cartHref = serializers.CharField(allow_blank=True, required=False)
    heroImage = serializers.CharField(allow_null=True, required=False)
    heroAlt = serializers.CharField(allow_blank=True, required=False)
    heroEnglish = serializers.CharField(allow_blank=True, required=False)
    heroTitle = serializers.CharField(allow_blank=True, required=False)
    heroTagline = serializers.CharField(allow_blank=True, required=False)
    heroVideo = serializers.CharField(allow_blank=True, required=False)
    heroCatalogHref = serializers.CharField(allow_blank=True, required=False)
    heroCatalogLabel = serializers.CharField(allow_blank=True, required=False)
    navItems = ProductNavItemOutputSerializer(many=True)
    moarefiBlocks = ContentBlockOutputSerializer(many=True)
    moshakhasatBlocks = ContentBlockOutputSerializer(many=True)
    videoBlocks = ContentBlockOutputSerializer(many=True)
    specModels = SpecModelOutputSerializer(many=True)
    specDownloadHref = serializers.CharField(allow_blank=True, required=False)
    videoGallery = serializers.ListField(child=serializers.CharField())
    faqItems = FaqItemOutputSerializer(many=True)
    href = serializers.CharField()

    def _media_url(self, media, request):
        if not media:
            return None
        if media.media_type == ProductMedia.TYPE_IMAGE and media.image:
            return self._build_absolute_url(media.image.url, request)
        if media.media_type in {ProductMedia.TYPE_VIDEO, ProductMedia.TYPE_DOCUMENT} and media.file:
            return self._build_absolute_url(media.file.url, request)
        return None

    def _build_absolute_url(self, path, request):
        if request and path:
            return request.build_absolute_uri(path)
        return path

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

    def _hero_video(self, obj, request):
        if obj.hero_video_url:
            return self._build_absolute_url(obj.hero_video_url.url, request)
        if obj.demo_video_url:
            return self._build_absolute_url(obj.demo_video_url.url, request)
        return None

    def _hero_catalog_href(self, obj, request):
        if obj.hero_catalog_href:
            return self._build_absolute_url(obj.hero_catalog_href.url, request)
        if obj.brochure_url:
            return self._build_absolute_url(obj.brochure_url.url, request)
        return None

    def _hero_catalog_label(self, obj):
        if obj.hero_catalog_label:
            return obj.hero_catalog_label
        if obj.hero_catalog_href or obj.brochure_url:
            return "Catalog"
        return None

    def _spec_download_href(self, obj, request):
        if obj.spec_download_href:
            return self._build_absolute_url(obj.spec_download_href.url, request)
        if obj.datasheet_url:
            return self._build_absolute_url(obj.datasheet_url.url, request)
        return None

    def _blocks_by_section(self, obj, section):
        blocks = [block for block in obj.content_blocks.all() if block.section == section]
        return ProductContentBlockSerializer(blocks, many=True).data

    def _video_gallery(self, obj, request):
        videos = [
            item
            for item in obj.media.all()
            if item.media_type == ProductMedia.TYPE_VIDEO
            and item.role == ProductMedia.ROLE_GALLERY
        ]
        return [self._media_url(item, request) for item in videos if self._media_url(item, request)]

    def to_representation(self, instance):
        request = self.context.get("request")
        hero_media = self._hero_image(instance)
        image_media = self._primary_image(instance)
        nav_items = ProductNavItemSerializer(instance.nav_items.all(), many=True).data
        spec_models = ProductSpecModelSerializer(instance.spec_models.all(), many=True).data
        faq_items = ProductFaqItemSerializer(instance.faq_items.all(), many=True).data

        return {
            "slug": instance.slug,
            "title": instance.title,
            "image": self._media_url(image_media, request),
            "price": instance.price,
            "description": instance.description or None,
            "highlight": self._highlight(instance),
            "highlightHtml": self._highlight_html(instance),
            "summaryHtml": self._summary_html(instance),
            "category": self._category_name(instance),
            "categoryHref": self._category_href(instance),
            "cartHref": instance.cart_href or None,
            "heroImage": self._media_url(hero_media, request),
            "heroAlt": self._hero_alt(instance, hero_media),
            "heroEnglish": self._hero_english(instance),
            "heroTitle": self._hero_title(instance),
            "heroTagline": instance.hero_tagline or None,
            "heroVideo": self._hero_video(instance, request),
            "heroCatalogHref": self._hero_catalog_href(instance, request),
            "heroCatalogLabel": self._hero_catalog_label(instance),
            "navItems": nav_items,
            "moarefiBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_MOAREFI),
            "moshakhasatBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_MOSHAKHASAT),
            "videoBlocks": self._blocks_by_section(instance, ProductContentBlock.SECTION_VIDEO),
            "specModels": spec_models,
            "specDownloadHref": self._spec_download_href(instance, request),
            "videoGallery": self._video_gallery(instance, request),
            "faqItems": faq_items,
            "href": f"/products/{instance.slug}",
        }


class ProductCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )
    media = ProductMediaCreateSerializer(many=True, required=False)
    features = ProductFeatureCreateSerializer(many=True, required=False)
    specifications = ProductSpecificationCreateSerializer(many=True, required=False)
    nav_items = ProductNavItemCreateSerializer(many=True, required=False)
    content_blocks = ProductContentBlockCreateSerializer(many=True, required=False)
    spec_models = ProductSpecModelCreateSerializer(many=True, required=False)
    faq_items = ProductFaqItemCreateSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
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
            "price",
            "highlight",
            "highlight_html",
            "summary_html",
            "hero_title",
            "hero_tagline",
            "hero_english",
            "hero_alt",
            "hero_video_url",
            "hero_catalog_href",
            "hero_catalog_label",
            "cart_href",
            "spec_download_href",
            "meta_title",
            "meta_description",
            "is_featured",
            "status",
            "published_at",
            "categories",
            "media",
            "features",
            "specifications",
            "nav_items",
            "content_blocks",
            "spec_models",
            "faq_items",
        )

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        media_list = validated_data.pop("media", [])
        feature_list = validated_data.pop("features", [])
        specification_list = validated_data.pop("specifications", [])
        nav_item_list = validated_data.pop("nav_items", [])
        content_block_list = validated_data.pop("content_blocks", [])
        spec_model_list = validated_data.pop("spec_models", [])
        faq_item_list = validated_data.pop("faq_items", [])

        product = Product.objects.create(**validated_data)
        if categories:
            product.categories.set(categories)

        for media_data in media_list:
            ProductMedia.objects.create(product=product, **media_data)

        for feature_data in feature_list:
            ProductFeature.objects.create(product=product, **feature_data)

        for specification_data in specification_list:
            ProductSpecification.objects.create(product=product, **specification_data)

        for nav_item_data in nav_item_list:
            ProductNavItem.objects.create(product=product, **nav_item_data)

        for block_data in content_block_list:
            item_list = block_data.pop("items", [])
            media_data = block_data.pop("media", None)
            media = None
            if media_data:
                media = ProductMedia.objects.create(product=product, **media_data)
            block = ProductContentBlock.objects.create(
                product=product,
                media=media,
                **block_data,
            )
            for item_data in item_list:
                ProductContentBlockItem.objects.create(block=block, **item_data)

        for spec_model_data in spec_model_list:
            spec_items = spec_model_data.pop("spec_items", [])
            spec_model = ProductSpecModel.objects.create(product=product, **spec_model_data)
            for spec_item_data in spec_items:
                ProductSpecItem.objects.create(spec_model=spec_model, **spec_item_data)

        for faq_item_data in faq_item_list:
            ProductFaqItem.objects.create(product=product, **faq_item_data)

        return product
