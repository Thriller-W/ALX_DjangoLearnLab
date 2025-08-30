from django.db.models import Q
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.views.generic import ListView
from .models import Post


class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()


class TagPostListView(ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs["tag_name"])
        return Post.objects.filter(tags__name=self.tag).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context

