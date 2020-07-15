import factory 
from django.contrib.auth import get_user_model

from ..models import Post, Tag 

User = get_user_model() 


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User 
    
    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f'user{n}@email.com')
    


class PostFactory(factory.django.DjangoModelFactory): 
    class Meta:
        model = Post 

    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n : f'title {n}' )



class TagFactory(factory.django.DjangoModelFactory): 
    class Meta:
        model = Tag 
    
    @factory.post_generation
    def posts(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for post in extracted:
                self.posts.add(post)