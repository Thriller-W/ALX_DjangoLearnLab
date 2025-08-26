from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import RegistrationForm, ProfileForm, PostForm
from .models import Post


def register_view(request):
    """
    Handles user registration.
    Uses CSRF protection via {% csrf_token %} in the template.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "Registration successful.")
            login(request, user)
            return redirect('profile')
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {"form": form})


@login_required
def profile_view(request):
    """
    Allows authenticated users to view and edit their profile.
    Critically: handles POST to update user information (email, first/last name).
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {"form": form})


# =====================================================
# ✅ BLOG POST CRUD VIEWS
# =====================================================

class PostListView(ListView):
    """Displays all blog posts."""
    model = Post
    context_object_name = "posts"
    template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    """Displays a single blog post."""
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create posts."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # Automatically set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows only authors to update their posts."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows only authors to delete their posts."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

