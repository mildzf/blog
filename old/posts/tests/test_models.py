from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Post 


class TestPostModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            published=True
        )
        self.post1 = Post.objects.create(
            title="Unpublished Test Post",
            slug="unpublished-test-post",
            content="This is an unpublished test post",
            author=self.user,
            published=False
        )

    
    def test_get_absolute_url(self):
        url = self.post.get_absolute_url()
        reversed_url = reverse('posts:detail', kwargs={'slug':self.post.slug})
        self.assertEqual(url, reversed_url)

    def test_is_published_on_published_post(self):
        self.assertTrue(self.post.is_published())

    def test_is_published_on_unpublished_post(self):
        self.assertFalse(self.post1.is_published())


