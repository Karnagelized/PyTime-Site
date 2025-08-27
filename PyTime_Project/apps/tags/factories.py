
import factory.django
from apps.tags.models import Tag



class TagFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации Тегов статей и проектов
    """

    name = factory.Sequence(lambda n: f"tag_{n}")


    class Meta:
        model = Tag
