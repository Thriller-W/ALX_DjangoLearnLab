# api/serializers.py
from datetime import date
from rest_framework import serializers
from .models import Author, Book

"""
Serializers for advanced API development:
- BookSerializer: serializes all Book fields; includes custom validation to ensure
  `publication_year` is not in the future.
- AuthorSerializer: includes the author's name AND a nested list of related books
  using BookSerializer with `many=True`.

Nested relationship explanation:
Because Book.author uses `related_name="books"`, we can access the reverse relation
as `author.books`. We expose that on AuthorSerializer as a read-only nested field:
`books = BookSerializer(many=True, read_only=True)`.
"""

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model including the FK to Author.
    Custom validation ensures `publication_year` is not in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author and nests all their related books.
    `books` uses the reverse relation created by `related_name="books"` on Book.author.
    It's read-only here; you can post/put books via Book endpoints or a custom create().
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]

