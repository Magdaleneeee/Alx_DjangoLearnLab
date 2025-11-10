# ALX-friendly views.py (includes register)
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Book, Library

# Function-based view: list all books and render template
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Optional plain-text version for debugging (not used by URLs)
def list_books_text(request):
    books = Book.objects.all()
    response = "List of Books:\n"
    for book in books:
        response += f"{book.title} by {book.author.name}\n"
    return HttpResponse(response, content_type="text/plain")

# Class-based detail view for a specific Library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Registration view using Django's UserCreationForm
def register(request):
    """
    Handle user registration. On success, log the user in and redirect to books list.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

# helper check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin view (only Admin role)
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})


# Librarian view (only Librarian role)
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})


# Member view (only Member role)
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})
