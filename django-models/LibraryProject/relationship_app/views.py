from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.http import HttpResponse
from .models import Book, Library


# ---------------- Existing Views ----------------

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# ---------------- Library Detail View ----------------

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all books belonging to this library
        context['books'] = Book.objects.filter(libraries=self.object)
        return context


# ---------------- Register View ----------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')  # redirect after successful register
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ---------------- Role-based Views ----------------

def is_admin(user):
    return user.is_superuser

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

def is_member(user):
    return user.groups.filter(name='Member').exists()


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# ---------------- Step 2: Secured Book Actions ----------------

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # Secured placeholder for adding a book
    return HttpResponse("Add book: permission check passed.")


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Secured placeholder for editing a book
    return HttpResponse(f"Edit book {book.pk}: permission check passed.")


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Secured placeholder for deleting a book
    return HttpResponse(f"Delete book {book.pk}: permission check passed.")

