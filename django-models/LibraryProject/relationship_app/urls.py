from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import admin_view, librarian_view, member_view, LibraryDetailView

urlpatterns = [
    # Books list
    path('books/', views.list_books, name='list_books'),

    # Library detail
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Role-based access
    path('admin-area/', admin_view, name='admin_view'),
    path('librarian-area/', librarian_view, name='librarian_view'),
    path('member-area/', member_view, name='member_view'),
]




