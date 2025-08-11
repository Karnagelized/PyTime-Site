
import factory.django
from apps.projects.models import Project
from numpy.random import random_integers
from apps.tags.factories import TagFactory


# Фабрика для генерации информации о Проекте
class ProjectFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: f"projectSlug_{n}")


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
        model = Project
