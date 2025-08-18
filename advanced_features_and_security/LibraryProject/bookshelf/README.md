# Bookshelf app - Permissions & Groups (README)

This app demonstrates custom model permissions and group-based access control.

## Files added/changed
- `models.py` — defines `Book` model with custom permissions: `can_view`, `can_create`, `can_edit`, `can_delete`.
- `forms.py` — `BookForm` for create/edit.
- `views.py` — views protected with `permission_required`.
- `urls.py` — app routes including `add_book/`, `edit_book/`, `delete_book/`.

## How to install & run (quick)
1. Ensure `bookshelf` is added to `INSTALLED_APPS` in `LibraryProject/settings.py`.
2. Create migrations and migrate:
   ```bash
   python manage.py makemigrations bookshelf
   python manage.py migrate
