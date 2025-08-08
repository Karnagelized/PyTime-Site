
import factory.django
from apps.tags.models import Tag


# Фабрика для генерации тегов для Статей и Проектов
class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"tag_{n}")


    class Meta:
        model = Tag
