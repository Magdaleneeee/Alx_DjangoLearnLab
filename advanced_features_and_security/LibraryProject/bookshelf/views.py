from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})
# ------------------------------------------
# Secure Views with Permissions and Safe Queries
# ------------------------------------------
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .models import Book

# View to securely list and search books
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    query = request.GET.get('q', '')
    if query:
        # Use ORM filtering to prevent SQL injection
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# View to securely create a new book (permission required)
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # For now, just render the form template
    return render(request, 'bookshelf/form_example.html')
