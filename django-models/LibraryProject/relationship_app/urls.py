# LibraryProject/relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: lists all books
    path('books/', list_books, name='list_books'),

    # Class-based view: library detail (use primary key)
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
