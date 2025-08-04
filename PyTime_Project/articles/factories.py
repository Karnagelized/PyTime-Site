
import factory.django
from articles.models import Article
from numpy.random import random_integers
from tags.factories import TagFactory


# Фабрика для генерации информации о Статье
class ArticleFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: f"articleSlug_{n}")


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
