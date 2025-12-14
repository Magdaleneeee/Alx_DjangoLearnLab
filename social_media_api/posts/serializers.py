from rest_framework import serializers
from .models import Post, Comment

#Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

#Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'content',
            'created_at',
            'updated_at',
        ]
