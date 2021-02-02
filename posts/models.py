from django.db import models
from django.utils import timezone 
from django.conf import settings
from django.urls import reverse 


User = settings.AUTH_USER_MODEL


class PostsManager(models.Manager):

    def active_posts(self):
        return self.filter(published=True)


class Post(models.Model): 
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True) 
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False) 
    author =  models.ForeignKey(
        User, related_name="posts", on_delete=models.CASCADE)
    objects = PostsManager()

    class Meta:
        ordering = ['-pub_date', '-created_on']

    def __str__(self):
        return self.title 

    def is_published(self):
        return self.published 
    is_published.boolean = True 

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    


