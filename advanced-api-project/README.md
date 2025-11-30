# Generic Views for Book (DRF)

This project implements Django REST Framework generic views to expose CRUD operations:

Endpoints:
- GET /api/books/                  -> BookListView (AllowAny)
- GET /api/books/<pk>/             -> BookDetailView (AllowAny)
- POST /api/books/create/          -> BookCreateView (IsAuthenticated)
- PUT/PATCH /api/books/<pk>/update/ -> BookUpdateView (IsAuthenticated)
- DELETE /api/books/<pk>/delete/   -> BookDeleteView (IsAuthenticated)

Filtering:
- /api/books/?author=<id>
- /api/books/?year=<year>

Validation:
- publication_year cannot be in the future (BookSerializer)

Permissions:
- Read-only for unauthenticated users
- Create, update, delete restricted to authenticated users
