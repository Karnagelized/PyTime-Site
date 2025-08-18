
from django.test import TestCase
from apps.skills.factories import HardSkillsFactory, HardSkillsCategoryFactory


# Тестирование модели скиллов
class HardSkillsModelTestCase(TestCase):
    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        hardSkills = HardSkillsFactory(
            name='HardSkillsName',
        )

        self.assertEquals(hardSkills.__str__(), 'HardSkillsName')


# Тестирование Админки для модели скиллов
class AdminHardSkillsTestCase(TestCase):
    def test_display_skills(self):
        """
            Тестирование вывода скиилов
        """

        hardSkillsCategory = HardSkillsCategoryFactory(
            skills=[
                HardSkillsFactory(name='Skill_1'),
                HardSkillsFactory(name='Skill_2')
            ]
        )

        self.assertEquals(hardSkillsCategory.getSkills(), 'Skill_1, Skill_2')
