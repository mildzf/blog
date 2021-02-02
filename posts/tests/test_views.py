from django.contrib.auth import get_user_model
from django.test import TestCase 
from django.urls import reverse

from posts.models import Post 

class TestDetailView(TestCase): 

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

    def test_published_post_is_displayed(self):
        url = reverse('posts:detail', kwargs={'slug':self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unpublished_post_is_not_displayed(self):
        url = reverse('posts:detail', kwargs={'slug':self.post1.slug})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_correct_template_is_used(self):
        url = reverse('posts:detail', kwargs={'slug':self.post.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'posts/post_detail.html')





class TestListView(TestCase):

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


    def test_only_published_posts_are_displayed(self):
        url = reverse('posts:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        total_posts = Post.objects.count()
        self.assertEqual(total_posts, 2)
        self.assertEqual(len(response.context['post_list']), 1)

    def test_correct_template_is_used(self):
        url = reverse('posts:list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'posts/post_list.html')
        