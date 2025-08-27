
import factory.django
from apps.articles.models import Article
from numpy.random import random_integers
from apps.tags.factories import TagFactory
from apps.users.factories import UserCustomFactory



class ArticleFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации Статьи
    """

    slug = factory.Sequence(lambda n: f"articleSlug_{n}")
    image = factory.django.ImageField()


    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.set(extracted)
        else:
            self.tags.set([])


    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.set(extracted)
        else:
            self.tags.set(TagFactory.create_batch(random_integers(10)))


    class Meta:
        model = Article
