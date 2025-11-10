```markdown
# Retrieve Book

```python
from bookshelf.models import Book
books = Book.objects.all()
for book in books:
    print(book)
# Output: 1984 by George Orwell (1949)
