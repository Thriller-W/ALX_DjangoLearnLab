# Advanced API Project — DRF Generic Views

## Views Implemented (api/views.py)
- `BookListView` (**ListView**): public GET `/api/books/`
  - Filters: `?author=<text>&title=<text>`
- `BookDetailView` (**DetailView**): public GET `/api/books/<int:pk>/`
- `BookCreateView` (**CreateView**): auth POST `/api/books/create/`
  - Custom validation: unique `title` example in `perform_create`
- `BookUpdateView` (**UpdateView**): auth PUT/PATCH `/api/books/<int:pk>/update/`
- `BookDeleteView` (**DeleteView**): auth DELETE `/api/books/<int:pk>/delete/`

## Permissions
- Read-only endpoints: `AllowAny`
- Write endpoints: `IsAuthenticated`

## URLs
- App: `api/urls.py`
- Project include: `advanced_project/urls.py` → `path("api/", include("api.urls"))`

## Testing (Windows)
Use `curl.exe` or Postman. For write actions, authenticate with your Django superuser.

## Notes
- Adjust serializer fields to match your `BookSerializer`.
- The `perform_create` and `perform_update` hooks show where to add custom behavior.
