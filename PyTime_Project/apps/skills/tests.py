
from django.test import TestCase
from apps.skills.factories import HardSkillsFactory, HardSkillsCategoryFactory



class HardSkillsModelTestCase(TestCase):
    """
        Тестирование модели Скиллов
    """

    def test_str_dunder(self):
        """
            Тестируем правильный вывод str метода
        """

        hardSkills = HardSkillsFactory(
            name='HardSkillsName',
        )

        self.assertEquals(hardSkills.__str__(), 'HardSkillsName')



class AdminHardSkillsTestCase(TestCase):
    """
        Тестирование Админки для модели Скиллов
    """

    def test_display_skills(self):
        """
            Тестирование вывода Скиллов
        """

        hardSkillsCategory = HardSkillsCategoryFactory(
            skills=[
                HardSkillsFactory(name='Skill_1'),
                HardSkillsFactory(name='Skill_2')
            ]
        )

        self.assertEquals(hardSkillsCategory.getSkills(), 'Skill_1, Skill_2')
