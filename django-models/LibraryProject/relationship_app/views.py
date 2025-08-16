from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test, login_required
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
        context['books'] = Book.objects.filter(library=self.object)
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

