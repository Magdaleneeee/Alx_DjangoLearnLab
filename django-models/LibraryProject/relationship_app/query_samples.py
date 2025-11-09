import os
import sys

# Get the directory of this file (.../LibraryProject/relationship_app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory (.../LibraryProject) to Python's path
sys.path.insert(0, BASE_DIR)

# Tell Django where to find your settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
author_name = "J.K. Rowling"
books_by_author = Book.objects.filter(author__name=author_name)
print(f"Books by {author_name}:")
for book in books_by_author:
    print("-", book.title)

# 2️⃣ List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"\nBooks in {library_name}:")
    for book in library.books.all():
        print("-", book.title)
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")

# 3️⃣ Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"\nLibrarian for {library_name}: {librarian.name}")
except Exception:
    print(f"No librarian assigned to {library_name}.")
