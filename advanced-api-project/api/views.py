from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    CRUD for Author. AuthorSerializer includes nested books (read-only).
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD for Book. BookSerializer enforces publication_year validation.
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
