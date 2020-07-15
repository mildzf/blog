import datetime 
import pytest
from pytest_django.asserts import assertTemplateUsed
from django.test import TestCase 
from django.urls import reverse 
from django.utils import timezone

from .factories import PostFactory, TagFactory, UserFactory
from ..models import Post
from ..views import PostDetailView, PostListView, TagDetailView


class TestPostDetailView(TestCase): 

    def setUp(self):
        self.user = UserFactory(username="Mylo")
        self.post = PostFactory(title="hello world", author=self.user)
        

    def test_view_is_at_the_correct_url(self):
        url = f'/{self.post.slug}/'
        response = self.client.get(url)
        assert response.status_code == 200

    def test_view_can_be_called_by_url_name(self):
        url = reverse("posts:detail", kwargs={'slug': self.post.slug})
        response = self.client.get(url)
        assert response.status_code == 200 

    def test_correct_template_is_used(self):
        url = reverse("posts:detail", kwargs={'slug': self.post.slug}) 
        response = self.client.get(url)
        assertTemplateUsed(response, 'posts/post_detail.html')
 
    def test_post_is_passed_into_context(self):
        url = reverse("posts:detail", kwargs={'slug': self.post.slug}) 
        response = self.client.get(url)
        assert 'hello world' in response.context['post'].title
 
    def test_404_on_not_found_post(self):
        url = reverse("posts:detail", kwargs={'slug': 'non-existing-post'}) 
        response = self.client.get(url)
        assert response.status_code == 404

    def test_does_not_display_unpublished_post(self):
         # Base test. make sure it works with published post
        post = PostFactory(title='published post', published=True)
        url = reverse("posts:detail", kwargs={'slug': post.slug}) 
        response = self.client.get(url)
        assert response.status_code == 200 
         
         # now test with unpublished post
        post1 = PostFactory(title='unpublished post', published=False)
        url = reverse("posts:detail", kwargs={'slug': post1.slug}) 
        response = self.client.get(url)
        assert response.status_code == 404

    def test_does_not_display_future_post(self):
        future_date = timezone.now() + datetime.timedelta(days=1)
        post1 = PostFactory(title='unpublished post', pub_date=future_date)
        url = reverse("posts:detail", kwargs={'slug': post1.slug}) 
        response = self.client.get(url)
        assert response.status_code == 404


class TestPostListView(TestCase):

    def setUp(self):
        self.future_date = timezone.now() + datetime.timedelta(days=1)
        self.posts = PostFactory.create_batch(5, published=True)
        self.posts += PostFactory.create_batch(3, published=False)
        self.posts += PostFactory.create_batch(2, pub_date=self.future_date)


    def test_view_available_at_correct_url(self):
        url = "/"
        response = self.client.get(url)
        assert response.status_code == 200 

    def test_view_can_be_called_by_url_name(self):
        url = reverse("posts:list")
        response = self.client.get(url)
        assert response.status_code == 200 

    def test_correct_template_is_used(self):
        url = reverse("posts:list")
        response = self.client.get(url)
        assertTemplateUsed(response, 'posts/post_list.html')

    def test_only_published_posts_returned_at_the_url(self):
        url = reverse("posts:list")
        response = self.client.get(url)

        # checks that published posts are not future and published==True
        published_posts = [i for i in self.posts if i.is_published() and not i.is_future()]
        assert len(response.context['posts']) == len(published_posts)

    

class TestTagDetailView(TestCase): 

    def setUp(self):
        self.posts = PostFactory.create_batch(7)
        self.posts1 = PostFactory.create_batch(3)
        self.tag = TagFactory(slug="mango")
        for post in self.posts:
            self.tag.posts.add(post)
        self.tag1 = TagFactory(slug="banana")
        for post in self.posts1:
            self.tag1.posts.add(post )
 
    def test_view_is_available_at_correct_url(self): 
        url = f'/tag/{self.tag.slug}/'
        response = self.client.get(url)
        assert response.status_code == 200
    
    def test_view_can_be_called_by_name(self): 
        url = reverse("posts:tag_detail", kwargs={'slug':self.tag.slug})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_correct_template_is_used(self):
        url = reverse("posts:tag_detail", kwargs={'slug': self.tag.slug})
        response = self.client.get(url)
        assertTemplateUsed(response, 'posts/tag_detail.html')

    def test_pagination(self):
        url = reverse("posts:tag_detail", kwargs={'slug': self.tag.slug})
        response = self.client.get(url)

        # check for pagination
        assert response.context['is_paginated'] == True

        # test first page
        assert len(response.context['object_list']) == 5
        
        # test second page
        url2 = url + "?page=2"
        response = self.client.get(url2)
        assert len(response.context['object_list']) == 2

    def test_view_only_returns_tagged_posts(self):
        url = reverse("posts:tag_detail", kwargs={'slug': self.tag1.slug})
        response = self.client.get(url)
        all_posts = Post.objects.all()
        tagged = []
        for post in all_posts:
            if self.tag1 in post.tags.all():
                tagged.append(post)
        assert len(all_posts) > len(tagged)
        assert len(response.context['object_list']) == len(tagged)
