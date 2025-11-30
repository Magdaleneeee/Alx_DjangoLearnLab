# api/views.py
"""
Generic views for Book model using Django REST Framework generics.
This file provides:
 - BookListView    : list all books (read-only for unauthenticated users)
 - BookDetailView  : retrieve a single book by pk (read-only)
 - BookCreateView  : create a new Book (authenticated users only)
 - BookUpdateView  : update a Book (authenticated users only)
 - BookDeleteView  : delete a Book (authenticated users only)
 
Customization details:
 - List view supports simple query params for filtering:
     ?author=<author_id>   -> filter by author id
     ?year=<publication_year> -> filter by publication year
 - Create/Update views rely on the BookSerializer for validation (publication_year check).
 - Create/Update override perform_create/perform_update hooks if you need extra behavior.
 - Permissions:
     - List/Detail: AllowAny (read-only)
     - Create/Update/Delete: IsAuthenticated
"""

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a paginated list of books (or full list depending on your settings).
    Accepts optional query params:
      - author=<author_id>       (filter books by author id)
      - year=<publication_year>  (filter books by publication year)
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally filter queryset by 'author' or 'year' query params.
        Keep the default ordering by newest first.
        """
        qs = super().get_queryset()
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        if author:
            qs = qs.filter(author_id=author)
        if year:
            try:
                year_int = int(year)
                qs = qs.filter(publication_year=year_int)
            except ValueError:
                # ignore invalid year filter (alternatively, raise a 400)
                pass
        return qs


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/
    Retrieve a single Book by primary key.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Create a new Book. Only authenticated users can create.
    Uses BookSerializer which handles validation of publication_year.
    If you need to link the created book to request.user or apply other rules,
    override perform_create() here.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Hook to customize save behavior. Right now we just save normally.
        You could, for example, set an extra field automatically:
            serializer.save(created_by=self.request.user)
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/update/
    Update an existing Book. Only authenticated users can update.
    Uses BookSerializer for validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook for custom update logic. For example, log the user who updated:
            serializer.save(updated_by=self.request.user)
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/
    Delete a Book. Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
