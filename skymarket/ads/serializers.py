from typing import List

from rest_framework import serializers

from .models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(max_length=30, read_only=True)
    author_last_name = serializers.CharField(max_length=35, read_only=True)
    author_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "pk",
            "text",
            "author_id",
            "created_at",
            "author_first_name",
            "author_last_name",
            "ad_id",
            "author_image",
        ]

    def get_fields(self):
        data = getattr(self, "instance", None)

        if isinstance(data, List):
            for obj in data:
                author = getattr(obj, 'author', None)

                obj.author_first_name = author.first_name
                obj.author_last_name = author.last_name
                obj.author_image = author.image
        elif data:
            author = getattr(data, 'author', None)

            self.instance.author_first_name = author.first_name
            self.instance.author_last_name = author.last_name
            self.instance.author_image = author.image


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
