from rest_framework import viewsets, generics, permissions
from .models import Book
from .serializers import BookSerializer

# BookViewSet uses IsAuthenticatedOrReadOnly permission.
# - Anyone can view books
# - Only authenticated users with a valid token can POST/PUT/PATCH/DELETE
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

    # Only authenticated users can create/update/delete; anyone can read
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # keep public read-only list
