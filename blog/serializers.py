from rest_framework import serializers

from .models import Blog, Category, RootCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class RootCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = RootCategory
        fields = ("id", "name", "slug", "categories")


class BlogListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "slug",
            "image",
            "excerpt",
            "categories",
            "published_at",
        )

    def get_image(self, obj):
        if obj.image:
            return self._build_absolute_url(obj.image.url)
        return None

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path


class BlogDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "slug",
            "image",
            "excerpt",
            "body",
            "categories",
            "published_at",
        )

    def get_image(self, obj):
        if obj.image:
            return self._build_absolute_url(obj.image.url)
        return None

    def _build_absolute_url(self, path):
        request = self.context.get("request")
        if request and path:
            return request.build_absolute_uri(path)
        return path
