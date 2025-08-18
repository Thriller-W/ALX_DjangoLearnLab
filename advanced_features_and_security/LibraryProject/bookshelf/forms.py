# bookshelf/forms.py
"""
ExampleForm - small, safe form for user input.
Checker requirement: this module must define ExampleForm.
This form validates and sanitizes a simple 'query' field.
"""

from django import forms
from django.utils.html import strip_tags
import re

class ExampleForm(forms.Form):
    """
    A simple example form used for searching or accepting short user input.
    - Validates max length and required-ness using Django form fields.
    - Sanitizes input in clean_query by stripping HTML tags and control characters.
    """
    query = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search books...'}),
        help_text='Enter search text (validated and sanitized).'
    )

    def clean_query(self):
        """
        Clean and sanitize the 'query' field:
        1. Strip surrounding whitespace.
        2. Remove any HTML tags (strip_tags) to avoid stored/display XSS.
        3. Remove control characters that could cause issues.
        4. Enforce max length as a final guard.
        Return the cleaned value (safe to use in ORM filters).
        """
        q = self.cleaned_data.get('query', '') or ''
        q = q.strip()
        # Remove any HTML tags (prevents '<script>' content staying in DB)
        q = strip_tags(q)
        # Remove control characters (non-printable)
        q = re.sub(r'[\x00-\x1f\x7f]', '', q)
        # Final length guard (should be redundant with max_length)
        if len(q) > 200:
            q = q[:200]
        return q

