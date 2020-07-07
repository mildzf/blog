from django.shortcuts import render
from django.views.generic import DetailView, ListView 

from .models import Post


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"



class PostListView(ListView):
    model = Post 
    context_object_name = "posts"
    paginate_by = 5
