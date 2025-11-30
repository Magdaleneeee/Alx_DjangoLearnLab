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

Filtering, search, and ordering:

- Filtering: ?author=<id>, ?publication_year=<year>, ?title=<value>
- Searching: ?search=<term>  (searches title and author name)
- Ordering: ?ordering=<field> (prefix with '-' for descending). Fields: title, publication_year, created_at

Examples:
  /api/books/?author=1&search=novel&ordering=-publication_year

Validation:
- publication_year cannot be in the future (BookSerializer)

Permissions:
- Read-only for unauthenticated users
- Create, update, delete restricted to authenticated users
