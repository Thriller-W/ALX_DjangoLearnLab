import os
import sys
import django

# Add the parent directory (where manage.py is) to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

# Set the correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def create_sample_data():
    author, _ = Author.objects.get_or_create(name='Jane Austen')
    book1, _ = Book.objects.get_or_create(title='Pride and Prejudice', author=author)
    book2, _ = Book.objects.get_or_create(title='Sense and Sensibility', author=author)

    other_author, _ = Author.objects.get_or_create(name='George Orwell')
    book3, _ = Book.objects.get_or_create(title='1984', author=other_author)

    library, _ = Library.objects.get_or_create(name='Central Library')
    library.books.add(book1, book3)

    Librarian.objects.get_or_create(library=library, defaults={'name': 'Mary Johnson'})

    return {
        'author': author,
        'book1': book1,
        'book2': book2,
        'book3': book3,
        'library': library,
    }


if __name__ == '__main__':
    objs = create_sample_data()

    # Query all books by a specific author
    author_name = 'Jane Austen'
    books_by_author = Book.objects.filter(author__name=author_name)
    print(f"\nBooks by author '{author_name}':")
    for b in books_by_author:
        print(" -", b.title)

    # List all books in a library
    library_name = 'Central Library'
    lib = Library.objects.get(name=library_name)
    print(f"\nBooks in library '{lib.name}':")
    for b in lib.books.all():
        print(" -", b.title)

    # Retrieve the librarian for a library
    try:
        librarian = lib.librarian
        print(f"\nLibrarian for library '{lib.name}': {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"\nNo librarian found for library '{lib.name}'")


