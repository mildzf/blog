from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from .mixins import PageLinksMixin
from .models import Post, Tag


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"



class PostListView(PageLinksMixin, ListView):
    model = Post 
    context_object_name = "posts"
    paginate_by = 5


class TagDetailView(SingleObjectMixin, PageLinksMixin, ListView):
    paginate_by = 5
    context_object_name = "posts"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.object
        return context

    def get_queryset(self):
        return self.object.posts.all()

        