from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields and validates publication_year isn't in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year ({value}) cannot be in the future (current year: {current_year})."
            )
        return value


class NestedBookSerializer(serializers.ModelSerializer):
    """
    Lightweight, read-only nested serializer for books displayed under authors.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'created_at']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author and includes nested books (read-only).
    Uses the 'books' related_name set on Book.author.
    """
    books = NestedBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']
