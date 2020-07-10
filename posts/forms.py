from django import forms
from pagedown.widgets import AdminPagedownWidget

from .models import Post, Tag


class PostForm(forms.ModelForm): 
    tags = forms.CharField(max_length=255, help_text='Enter each tag separated by a comma and a space. eg. "tag1, tag2"')
    content = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = Post 
        fields = ['title', 'image', 'content', 'tags', 'author', 'pub_date', 'published']

    def create_tags(self):
        tags_list = self.cleaned_data['tags'].split(', ')
        post = super(PostForm, self).save()
        for tag in tags_list:
            tag_name = tag.strip()
            new_tag = Tag.objects.get_or_create(slug=tag_name)[0]
            new_tag.posts.add(post.id)
            new_tag.save()