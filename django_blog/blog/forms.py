from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # Include email + optional name fields in registration
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]  # Author will be set automatically in the view
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter a title", "class": "form-control"}),
            "content": forms.Textarea(attrs={"rows": 6, "placeholder": "Write your post here...", "class": "form-control"}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

    def clean_content(self):
        data = self.cleaned_data.get('content', '')
        if not data or not data.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        if len(data) > 2000:
            raise forms.ValidationError("Comment too long (max 2000 characters).")
        return data.strip()
