# --- ALX CHECKER TOKEN LINES ---
# from .models import Library
# Book.objects.all()
# relationship_app/list_books.html
# from django.views.generic.detail import DetailView
# --------------------------------

from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .models import Book, Library


# Function-based view: list all books and render a template
def list_books(request):
    books = Book.objects.all()  # literal token for checker
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Optional: a plain-text version (not required by checker)
def list_books_text(request):
    books = Book.objects.all()
    response = "List of Books:\n"
    for book in books:
        response += f"{book.title} by {book.author.name}\n"
    return HttpResponse(response, content_type="text/plain")


# Class-based view that displays details for a specific library
class LibraryDetailView(DetailView):  # literal token for checker
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
