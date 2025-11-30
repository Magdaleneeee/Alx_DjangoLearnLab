# api/views.py

"""
Generic views for the Book model using Django REST Framework.

This file includes:
 - BookListView:        List all books (read allowed for everyone)
 - BookDetailView:      Retrieve a single book
 - BookCreateView:      Create a new book (authenticated only)
 - BookUpdateView:      Update a book (authenticated only)
 - BookDeleteView:      Delete a book (authenticated only)

Permissions:
 - ListView & DetailView → IsAuthenticatedOrReadOnly
 - Create, Update, Delete → IsAuthenticated

We use Django REST Framework generics for clean, efficient CRUD.
Filtering on ListView supports ?author=&?year=.
"""

from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Book
from .serializers import BookSerializer



from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    - Filtering via ?author=&?publication_year=&?title=
    - Search via ?search=keyword  (searches title and author name)
    - Ordering via ?ordering=title or ?ordering=-publication_year
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filterable fields
    filterset_fields = ['author', 'publication_year', 'title']

    # Searchable fields
    search_fields = ['title', 'author__name']

    # Orderable fields
    ordering_fields = ['title', 'publication_year', 'created_at']



class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<id>/
    Public read.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Authenticated users only.
    Uses serializer validation for publication_year.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Could add custom logic here (e.g., set created_by)
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /api/books/<id>/update/
    Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<id>/delete/
    Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
