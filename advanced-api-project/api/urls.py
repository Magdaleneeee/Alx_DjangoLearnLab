# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# If you still have viewsets elsewhere, keep the router below.
router = DefaultRouter()
# Example: router.register(r'books', views.BookViewSet, basename='book')  # only if BookViewSet exists

urlpatterns = [
    # Generic view endpoints (explicit, single-purpose paths)
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),

    # Optional: include router URLs if you also have viewsets
    path('', include(router.urls)),
]
