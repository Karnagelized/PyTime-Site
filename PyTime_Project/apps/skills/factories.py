
import factory.django
from apps.skills.models import HardSkills, HardSkillsCategory
from numpy.random import random_integers



class HardSkillsFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации Hard скиллов
    """

    name = factory.Sequence(lambda n: f"HardSkill_{n}")


    class Meta:
        model = HardSkills



class HardSkillsCategoryFactory(factory.django.DjangoModelFactory):
    """
        Фабрика для генерации категорий Hard скиллов
    """

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
