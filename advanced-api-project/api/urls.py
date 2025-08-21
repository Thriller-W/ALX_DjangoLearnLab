from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),                  # /api/books/
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),     # /api/books/1/
    path("books/create/", BookCreateView.as_view(), name="book-create"),       # /api/books/create/
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),   # /api/books/1/update/
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),   # /api/books/1/delete/
]
