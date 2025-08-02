from bookshelf.models import Book

# Delete a specific book with id 1
Book.objects.get(id=1).delete()

