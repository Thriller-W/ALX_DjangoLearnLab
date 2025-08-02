from bookshelf.models import Book

# Delete a specific book with id 1
book = Book.objects.get(id=1)
book.delete()

