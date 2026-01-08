from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductFaqItem,
    ProductGalleryImage,
    ProductSpecItem,
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
        image = root.image.url if root.image else None
        return {
            "id": root.id,
            "name": root.name,
            "slug": root.slug,
            "image": self._build_absolute_url(image),
        }

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


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
    image = serializers.SerializerMethodField()

    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug", "image")

    def get_image(self, obj):
        if not obj.image:
            return None
        return self._build_absolute_url(obj.image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class RootCategoryListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug", "image", "categories")

    def get_image(self, obj):
        if not obj.image:
            return None
        return self._build_absolute_url(obj.image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class ProductGalleryImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductGalleryImage
        fields = ("id", "url", "alt_text", "sort_order")

    def get_url(self, obj):
        if not obj.image:
            return None
        return self._build_absolute_url(obj.image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class ProductGalleryImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGalleryImage
        fields = ("image", "alt_text", "sort_order")


class ProductFaqItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFaqItem
        fields = ("question", "answer", "sort_order")


class ProductSpecItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecItem
        fields = ("variant_name", "label", "value", "sort_order")


class ProductListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    hero_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "short_description",
            "hero_image",
            "categories",
        )

    def get_hero_image(self, obj):
        if not obj.hero_image:
            return None
        return self._build_absolute_url(obj.hero_image.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class ProductDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    hero_image = serializers.SerializerMethodField()
    hero_video = serializers.SerializerMethodField()
    gallery_images = ProductGalleryImageSerializer(many=True, read_only=True)
    faq_items = ProductFaqItemSerializer(many=True, read_only=True)
    spec_table = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "categories",
            "short_description",
            "description",
            "hero_image",
            "hero_video",
            "gallery_images",
            "faq_items",
            "spec_table",
        )

    def get_hero_image(self, obj):
        if not obj.hero_image:
            return None
        return self._build_absolute_url(obj.hero_image.url)

    def get_hero_video(self, obj):
        if not obj.hero_video:
            return None
        return self._build_absolute_url(obj.hero_video.url)

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path

    def get_spec_table(self, obj):
        items = list(obj.spec_items.all())
        if not items:
            return {"columns": [], "rows": []}

        columns = []
        column_set = set()
        rows = []
        row_map = {}

        for item in items:
            if item.variant_name not in column_set:
                column_set.add(item.variant_name)
                columns.append(item.variant_name)
            row = row_map.get(item.label)
            if not row:
                row = {"label": item.label, "values": {}}
                row_map[item.label] = row
                rows.append(row)
            row["values"][item.variant_name] = item.value

        return {"columns": columns, "rows": rows}


class ProductCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )
    gallery_images = ProductGalleryImageCreateSerializer(many=True, required=False)
    faq_items = ProductFaqItemSerializer(many=True, required=False)
    spec_items = ProductSpecItemSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "title",
            "slug",
            "short_description",
            "description",
            "hero_image",
            "hero_video",
            "categories",
            "gallery_images",
            "faq_items",
            "spec_items",
        )

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        gallery_images = validated_data.pop("gallery_images", [])
        faq_items = validated_data.pop("faq_items", [])
        spec_items = validated_data.pop("spec_items", [])

        product = Product.objects.create(**validated_data)
        if categories:
            product.categories.set(categories)

        for image_data in gallery_images:
            ProductGalleryImage.objects.create(product=product, **image_data)

        for faq_data in faq_items:
            ProductFaqItem.objects.create(product=product, **faq_data)

        for spec_data in spec_items:
            ProductSpecItem.objects.create(product=product, **spec_data)

        return product
