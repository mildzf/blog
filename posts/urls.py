from django.urls import path 

from .views import PostDetailView, PostListView, TagDetailView


app_name="posts"

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('<slug:slug>/', PostDetailView.as_view(), name="detail"),
    path('tag/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
]