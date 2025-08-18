# LibraryProject/bookshelf/urls.py
from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]
