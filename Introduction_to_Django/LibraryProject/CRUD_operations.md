>>> from bookshelf.models import Book
>>> Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
# Expected output: <Book: 1984 by George Orwell (1949)>
>>> from bookshelf.models import Book
>>> Book.objects.all()
# Expected output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>
>>> book = Book.objects.get(title='1984')
>>> book.title = 'Nineteen Eighty-Four'
>>> book.save()
# Expected output: Title updated successfully to Nineteen Eighty-Four
>>> book = Book.objects.get(title='Nineteen Eighty-Four')
>>> book.delete()
>>> Book.objects.all()
# Expected output: <QuerySet []> (book deleted)
