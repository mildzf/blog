from django.contrib import admin

from .models import Post 


class PostAdmin(admin.ModelAdmin): 
    list_display = ['title', 'is_published', 'pub_date', 'created', 'updated']




admin.site.register(Post, PostAdmin)
