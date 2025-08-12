import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "Jane Austen"  # Example author name
author = Author.objects.get(name=author_name)  # Required exact code
books_by_author = Book.objects.filter(author=author)  # Required exact code

print(f"Books by {author_name}:")
for book in books_by_author:
    print(f"- {book.title}")

# List all books in a library
library_name = "Central Library"  # Example library name
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)  # This covers “Retrieve the librarian for a library.”
print(f"\nLibrarian for {library_name}: {librarian.name}")

