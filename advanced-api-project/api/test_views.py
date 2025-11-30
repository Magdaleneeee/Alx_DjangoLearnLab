"""
Unit tests for the advanced-api-project Book API views.

Location: advanced-api-project/api/test_views.py

How to run:
    cd advanced-api-project
    python manage.py test api

These tests use rest_framework.test.APITestCase to exercise the views that
were implemented using generic views and DRF filter backends.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

User = get_user_model()


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authenticated actions
        self.user = User.objects.create_user(username="tester", password="testpass123")

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create some books
        self.book1 = Book.objects.create(
            title="Alpha Book",
            publication_year=2000,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Beta Book",
            publication_year=2010,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Gamma Book",
            publication_year=2010,
            author=self.author2
        )

        # Base endpoints
        self.list_url = "/api/books/"
        self.create_url = "/api/books/create/"
        # detail/update/delete will use the pk in the path when needed

        # Simple client wrappers
        self.client = APIClient()

    # -------------------------
    # READ / LIST / DETAIL tests
    # -------------------------
    def test_list_books_anonymous(self):
        """Anonymous user can GET the list of books (200)."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Ensure we can see at least the created books
        # If pagination is enabled, results may be nested in "results"
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        else:
            results = data
        titles = {item["title"] for item in results}
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_retrieve_book_detail_anonymous(self):
        """Anonymous user can GET a book detail."""
        resp = self.client.get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["title"], self.book1.title)
        self.assertEqual(data["publication_year"], self.book1.publication_year)

    # -------------------------
    # FILTER / SEARCH / ORDER tests
    # -------------------------
    def test_filter_books_by_author(self):
        """Filtering by author id should return only that author's books."""
        resp = self.client.get(self.list_url, {"author": self.author1.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        else:
            results = data
        # all titles should be from author1
        for item in results:
            self.assertEqual(item["author"], self.author1.pk)

    def test_filter_books_by_publication_year(self):
        """Filtering by publication_year returns correct books."""
        resp = self.client.get(self.list_url, {"publication_year": 2010})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        else:
            results = data
        years = {item["publication_year"] for item in results}
        self.assertEqual(years, {2010})

    def test_search_books_by_title_and_author(self):
        """Search should match title and author__name fields."""
        # search by title substring
        resp = self.client.get(self.list_url, {"search": "Alpha"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        else:
            results = data
        titles = [item["title"] for item in results]
        self.assertIn("Alpha Book", titles)

        # search by author name
        resp2 = self.client.get(self.list_url, {"search": "Author Two"})
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        data2 = resp2.json()
        if isinstance(data2, dict) and "results" in data2:
            results2 = data2["results"]
        else:
            results2 = data2
        # Expect at least the book by author2
        titles2 = [item["title"] for item in results2]
        self.assertIn("Gamma Book", titles2)

    def test_ordering_books(self):
        """Ordering by title should change the order in the results."""
        resp = self.client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        else:
            results = data
        titles = [item["title"] for item in results]
        # titles should be sorted ascending by title when ordering=title
        self.assertEqual(titles, sorted(titles))

    # -------------------------
    # AUTHENTICATED CREATE / UPDATE / DELETE tests
    # -------------------------
    def test_create_book_unauthenticated_forbidden(self):
        """Anonymous users should not be able to create (401/403)."""
        payload = {"title": "New Book", "publication_year": 2021, "author": self.author1.pk}
        resp = self.client.post(self.create_url, payload, format="json")
        # Either 401 or 403 depending on auth setup; accept either
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated users can create a book (201) and book exists in DB."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Created Book", "publication_year": 2021, "author": self.author1.pk}
        resp = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        # ensure returned data includes the fields and DB has the object
        self.assertEqual(data["title"], "Created Book")
        self.assertTrue(Book.objects.filter(title="Created Book", author=self.author1).exists())

    def test_update_book_authenticated(self):
        """Authenticated users can update a book using the update endpoint."""
        self.client.force_authenticate(user=self.user)
        update_url = f"/api/books/{self.book1.pk}/update/"
        payload = {"title": "Alpha Book Updated", "publication_year": 2001, "author": self.author1.pk}
        resp = self.client.put(update_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # refresh from DB
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha Book Updated")
        self.assertEqual(self.book1.publication_year, 2001)

    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book using the delete endpoint."""
        self.client.force_authenticate(user=self.user)
        delete_url = f"/api/books/{self.book2.pk}/delete/"
        resp = self.client.delete(delete_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    def test_permissions_read_allowed_write_protected(self):
        """Sanity: read endpoints are available to anonymous, write endpoints require auth."""
        # anonymous read
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # anonymous create forbidden
        resp2 = self.client.post(self.create_url, {"title": "X", "publication_year": 2020, "author": self.author1.pk}, format="json")
        self.assertIn(resp2.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated create allowed
        self.client.force_authenticate(user=self.user)
        resp3 = self.client.post(self.create_url, {"title": "Y", "publication_year": 2020, "author": self.author1.pk}, format="json")
        self.assertEqual(resp3.status_code, status.HTTP_201_CREATED)
