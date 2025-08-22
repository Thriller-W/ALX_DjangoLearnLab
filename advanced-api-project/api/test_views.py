from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(title="Book One", author="Author A", publication_year=2020)
        self.book2 = Book.objects.create(title="Book Two", author="Author B", publication_year=2021)
        self.book3 = Book.objects.create(title="Another Book", author="Author A", publication_year=2022)

    def _books_list_url(self):
        return reverse("book-list")

    def _book_detail_url(self, pk):
        return reverse("book-detail", args=[pk])

    def test_list_books(self):
        url = self._books_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        items = data.get("results", data)
        self.assertGreaterEqual(len(items), 3)

    def test_retrieve_book(self):
        url = self._book_detail_url(self.book1.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["title"], "Book One")

    def test_create_book(self):
        url = self._books_list_url()
        payload = {"title": "New Book", "author": "Author C", "publication_year": 2023}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data["title"], "New Book")
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book(self):
        url = self._book_detail_url(self.book1.pk)
        payload = {"title": "Updated Book", "author": "Author A", "publication_year": 2020}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["title"], "Updated Book")
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book(self):
        url = self._book_detail_url(self.book2.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_filter_books_by_author(self):
        url = f"{self._books_list_url()}?author=Author A"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        items = data.get("results", data)
        self.assertTrue(all(book["author"] == "Author A" for book in items))

    def test_search_books_by_title(self):
        url = f"{self._books_list_url()}?search=Another"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        items = data.get("results", data)
        self.assertTrue(any("Another" in book["title"] for book in items))

    def test_order_books_by_publication_year(self):
        url = f"{self._books_list_url()}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        items = data.get("results", data)
        years = [book["publication_year"] for book in items]
        self.assertEqual(years, sorted(years, reverse=True))

