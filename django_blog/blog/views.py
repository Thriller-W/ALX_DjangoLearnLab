from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistrationForm, ProfileForm

def register_view(request):
    """
    Handles user registration.
    Uses CSRF protection via {% csrf_token %} in the template.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # email/first/last already bound via form; save the user
            user.save()
            messages.success(request, "Registration successful.")
            # Optionally auto-login then go to profile
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

