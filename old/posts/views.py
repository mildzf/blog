from django.shortcuts import render

from .author import AuthorListView, AuthorDetailView
from .models import Post 


class PostListView(AuthorListView):
    queryset = Post.objects.active_posts()
    template_name = "posts/post_list.html"
    


class PostDetailView(AuthorDetailView):
    queryset = Post.objects.active_posts()
    template_name = "posts/post_detail.html" 