>>> book = Book.objects.get(title='Nineteen Eighty-Four')
>>> book.delete()
>>> Book.objects.all()
# Expected output: <QuerySet []> (book deleted)
