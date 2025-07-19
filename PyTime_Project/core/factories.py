
import factory.django
from core.models import (
    CustomUser, Tag, Article, Project, HardSkills, HardSkillsCategory,
    Comment
)
from random import choice
from numpy.random import random_integers
from datetime import date

# Фабрика для генерации моделей Пользователей
class UserCustomFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj}_email@mail.ru")
    password = factory.LazyAttribute(lambda obj: f"password_{obj.username}")


    class Meta:
        model = CustomUser


# Фабрика для генерации тегов для Статей и Проектов
class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"tag_{n}")


    class Meta:
        model = Tag



# Фабрика для генерации информации о Статьи
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


# Фабрика для генерации информации о Проекте
class ProjectFactory(factory.django.DjangoModelFactory):
    slug = factory.Sequence(lambda n: f"projectSlug_{n}")


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


# Фабрика для генерации Hard скиллов
class HardSkillsFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"HardSkill_{n}")


    class Meta:
        model = HardSkills


# Фабрика для генерации категорий Hard скиллов
class HardSkillsCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"hardSkillsCategory_{n}")


    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.skills.set(extracted)
        else:
            self.skills.set(HardSkillsFactory.create_batch(random_integers(10)))


    class Meta:
        model = HardSkillsCategory


class CommentFactory(factory.django.DjangoModelFactory):
    contentSlug = factory.Sequence(lambda n: f"commentSlug_{n}")
    author = factory.SubFactory(UserCustomFactory)

    class Meta:
        model = Comment