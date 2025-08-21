# api/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListView
    GET /api/books/?author=<text>&title=<text>
    Public read-only: lists all books. Supports simple filtering via query params.
    """
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        author = self.request.query_params.get("author")
        title = self.request.query_params.get("title")
        if author:
            qs = qs.filter(author__icontains=author)
        if title:
            qs = qs.filter(title__icontains=title)
        return qs


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView
    GET /api/books/<int:pk>/
    Public read-only: retrieves a single book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


class BookCreateView(generics.CreateAPIView):
    """
    CreateView
    POST /api/books/create/
    Auth required: creates a new book.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        if title and Book.objects.filter(title=title).exists():
            raise ValidationError({"title": "A book with this title already exists."})
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView
    PUT/PATCH /api/books/<int:pk>/update/
    Auth required: updates an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView
    DELETE /api/books/<int:pk>/delete/
    Auth required: deletes an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

