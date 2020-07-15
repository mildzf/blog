from time import time
from django.conf import settings
from django.db import models
from django.urls import reverse 
from django.utils import timezone
from django.utils.text import slugify

from .utils import storage_location

User = settings.AUTH_USER_MODEL


class PostManager(models.Manager):
    def all(self):
        return self.filter(published=True).filter(pub_date__lte=timezone.now())


class Post(models.Model): 
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    image = models.ImageField(blank=True, upload_to=storage_location)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='posts',on_delete=models.CASCADE)
    published = models.BooleanField(default=True)
    objects = PostManager()

    class Meta:
        ordering = ['-pub_date', '-updated', '-created']

    def __str__(self):
        return self.title 

    def save(self, *args, **kwargs):
       time_now = "".join(str(time()).split('.'))[7:]  # create time string minus first 7 chars
       slug_string = f"{self.title}-{time_now}"  # combine with title in an f-string
       self.slug = slugify(slug_string)  # create a unique slug
       super(Post, self).save(*args, **kwargs) # Call the real save() method
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def is_published(self):
        return self.published
    is_published.boolean = True

    def is_future(self):
        if self.pub_date > timezone.now():
            return True
        return False
    is_future.boolean=True


class Tag(models.Model): 
    slug = models.SlugField(max_length=55)
    posts = models.ManyToManyField('Post', related_name='tags')

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug 
    
    def get_absolute_url(self):
        return reverse('posts:tag_detail', kwargs={'slug': self.slug})