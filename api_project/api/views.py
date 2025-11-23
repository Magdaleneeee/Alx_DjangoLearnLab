from rest_framework import viewsets, generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Book available via router (e.g. /api/books_all/).
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # easier for testing

class BookList(generics.ListAPIView):
    """
    Existing read-only list endpoint (keeps /books/ working).
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
