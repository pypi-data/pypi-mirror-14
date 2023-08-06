import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from ..models import Tag, TaggedItem
from .models import TagTestArticle0, TagTestArticle1


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    last_name = 'John'
    first_name = 'Doe'
    username = factory.sequence(lambda n: 'username{0}'.format(n))
    email = 'webmaster@example.com'
    password = make_password('password')
    last_login = timezone.now()


class TagTestArticle0Factory(factory.DjangoModelFactory):
    class Meta:
        model = TagTestArticle0

    title = 'Test article'


class TagTestArticle1Factory(factory.DjangoModelFactory):
    class Meta:
        model = TagTestArticle1

    title = 'Test article'


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('label',)

    label = factory.Sequence(lambda n: 'Tag {}'.format(n))


class TaggedItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = TaggedItem

    tag = factory.SubFactory(TagFactory)
    author = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(TagTestArticle0Factory)
