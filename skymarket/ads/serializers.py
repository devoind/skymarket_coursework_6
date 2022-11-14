from rest_framework import serializers

from .models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    ad_id = serializers.IntegerField(source='ad.id', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_image = serializers.ImageField(source='author.image', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'pk',
            'text',
            'author_id',
            'created_at',
            'ad_id',
            'author_first_name',
            'author_last_name',
            'author_image',
        )


class AdSerializer(serializers.ModelSerializer):
    # author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    # author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    # phone = serializers.CharField(source='author.phone', read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ad
        fields = (
            'pk',
            'title',
            'price',
            'author',
            'description',
            'image',
        )


class AdDetailSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)

    class Meta:
        model = Ad
        fields = ('pk', 'title', 'price', 'author', 'author_first_name')
