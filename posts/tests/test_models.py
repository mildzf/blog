import pytest
import datetime
from django.test import TestCase
from django.utils import timezone
from .factories import PostFactory, TagFactory, UserFactory

from ..models import Post


class TestPostModel(TestCase):

    def test_string_rendering(self):
       post = PostFactory(title="Hello world")
       assert post.__str__() == "Hello world"

    def test_get_absolute_url_returns_url(self):
        post = PostFactory(title="Hello world")
        assert post.get_absolute_url() == f"/{post.slug}/"

    def test_slug_is_auto_generated(self):
        author = UserFactory()
        author.save()
        post = Post.objects.create(author=author, title="Hello World")
        assert "hello-world" in post.slug

    def test_two_posts_of_similar_title_have_different_slugs(self):
        author = UserFactory(username="mylo")
        author.save()
        post1 = Post.objects.create(author=author, title="Hello -world")
        post2 = Post.objects.create(author=author, title="Hello world")
        assert post1.slug != post2.slug

    def test_is_published_returns_true_only_published_posts(self):
        posts = PostFactory.create_batch(3, published=True)
        posts += PostFactory.create_batch(2, published=False)
        published_posts = []
        for post in posts:
            if post.published == True:
                published_posts.append(post)
        assert len(published_posts) == 3


    def test_is_future_returns_true_only_future_posts(self):
        future_date = timezone.now() + datetime.timedelta(days=1)
        past_date = timezone.now() - datetime.timedelta(days=3)
        posts = PostFactory.create_batch(3, pub_date=future_date)
        posts += PostFactory.create_batch(2, pub_date=past_date)
        future_posts = []
        for post in posts:
            if post.is_future():
                future_posts.append(post)
        assert len(future_posts) == 3

class TestTagModel(TestCase): 

    def test_string_representation(self):
        post = PostFactory()
        tag = TagFactory(slug="worldboss", posts=(post,))
        assert tag.__str__() == 'worldboss'

    def test_get_absolute_url_returns_url(self):
        post = PostFactory()
        tag = TagFactory(slug="worldboss", posts=(post,))
        assert tag.get_absolute_url() == f"/tag/{tag.slug}/"

