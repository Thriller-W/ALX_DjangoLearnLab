# api/models.py
from django.db import models

"""
Models for an advanced API demo:
- Author: represents a writer with a simple name field.
- Book: represents a book with title, publication_year, and a ForeignKey to Author.

Relationship:
One Author -> Many Books (Author.books). We use `related_name="books"` so nested
serialization can access the reverse relation as `author.books`.
"""

class Author(models.Model):
    # The author's full name
    name = models.CharField(max_length=255, help_text="Full name of the author.")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)

    # Four-digit publication year (kept as IntegerField per requirement)
    publication_year = models.IntegerField()

    # One-to-many link: an Author can have many Books
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",  # critical for nested serialization
        help_text="The author who wrote this book."
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
