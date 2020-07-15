import pytest 
from django.test import TestCase 
from django.utils import timezone

from .factories import UserFactory
from ..forms import PostForm 
from ..models import Tag


class TestPostForm(TestCase): 
    
    def setUp(self):
        self.user = UserFactory(username="mylo")

    def test_form_with_valid_data(self):
        data = {
            "title": "hello world",
            "content": "this is a test post",
            "author": self.user,
            "tags": "test, django, post, hello",
            "published": True,
            "pub_date": timezone.now()
        }
        form = PostForm(data=data)
        assert form.is_valid()

    def test_form_with_invalid_data(self):
        data = {
            "title": "",
            "content": "this is a test post",
            "author": self.user,
            "tags": "test, django, post, hello",
            "published": True,
            "pub_date": timezone.now()
        }
        form = PostForm(data=data)
        assert not form.is_valid()

    def test_tag_creation(self):
        data = {
            "title": "hello world",
            "content": "this is a test post",
            "author": self.user,
            "tags": "test, django, post, hello",
            "published": True,
            "pub_date": timezone.now()
        }
        form = PostForm(data=data)
        form.save()

        # check that there are no tags present
        assert Tag.objects.count() == 0

        # create tags and check for their presence
        form.create_tags()
        assert Tag.objects.count() == 4
        


