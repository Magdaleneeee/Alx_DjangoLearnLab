from django.db import models

class Author(models.Model):
    """
    Represents an author. Minimal fields for clarity:
      - name: the author's full name.
    Relationship: An Author has many Book instances (one-to-many).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book:
      - title: title of the book.
      - publication_year: integer year, validated in the serializer.
      - author: ForeignKey to Author. related_name='books' provides author.books access.
      - created_at: auto timestamp to track creation.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
