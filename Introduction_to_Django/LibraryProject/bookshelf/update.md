# Update the Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
# Output: Title updated to "Nineteen Eighty-Four"
