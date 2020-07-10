from django.contrib import admin

from .forms import PostForm
from .models import Post 


class PostAdmin(admin.ModelAdmin): 
    list_display = ['title', 'is_published', 'is_future', 'pub_date', 'created', 'updated']
    list_filter = ['pub_date', 'updated']
    search_fields = ['title', 'content']
    ordering = ['-pub_date']
    form = PostForm 

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        try:
            tags = ",".join([str(i) for i in obj.tags.all()])
        except Exception:
            tags = None
        if tags:
            form.base_fields['tags'].initial = tags 
        form.base_fields['author'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        form.author = request.user
        form.save()
        form.create_tags()
        super(PostAdmin, self).save_model(request, obj, form, change)



admin.site.register(Post, PostAdmin)
