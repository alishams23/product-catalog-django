from rest_framework import serializers

from .models import (
    Category,
    Product,
    ProductGalleryImage,
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


class ProductCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False,
    )
    gallery_images = ProductGalleryImageCreateSerializer(many=True, required=False)

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
        )

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        gallery_images = validated_data.pop("gallery_images", [])

        product = Product.objects.create(**validated_data)
        if categories:
            product.categories.set(categories)

        for image_data in gallery_images:
            ProductGalleryImage.objects.create(product=product, **image_data)

        return product
