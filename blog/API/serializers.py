from rest_framework import serializers

from blog.models import Post


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id", "title", "content", "slug"
        )


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id", "title", "content",
        )


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]
