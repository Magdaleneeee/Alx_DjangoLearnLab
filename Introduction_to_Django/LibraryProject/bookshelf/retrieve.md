# Retrieve Book

book = Book.objects.get(title="1984")
book
# Output: <Book: 1984> with author="George Orwell" and publication_year=1949
