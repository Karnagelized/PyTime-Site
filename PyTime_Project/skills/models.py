
from django.db import models
from skills.managers import VisibleHardSkillsCategoryManager


# Модель для Hard скиллов
class HardSkills(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50, verbose_name='Название')
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Скилл'
        verbose_name_plural = 'Скиллы'


    def __str__(self):
        return (
            f'{self.name}'
        )

# Модель для категорий Hard скиллов
class HardSkillsCategory(models.Model):
    name = models.CharField(unique=True, blank=False, max_length=50, verbose_name='Название')
    position = models.PositiveSmallIntegerField(blank=False, default=0, verbose_name='Позиция')
    skills = models.ManyToManyField(HardSkills, blank=True)
    isVisible = models.BooleanField(default=True, verbose_name='Видимость')
    dateCreate = models.DateTimeField(blank=False, auto_now_add=True, verbose_name='Дата создания')

    # Стандартный менеджер представления
    objects = models.Manager()
    # Менеджер отображающий только "включенные" категории
    visibleCategory = VisibleHardSkillsCategoryManager()


    class Meta:
        verbose_name = 'Категория скилла'
        verbose_name_plural = 'Категории скиллов'


    # Метод для получения всех скиллов данной категории
    def getSkills(self):
        return ', '.join([skill.name for skill in self.skills.all() if skill.isVisible])


    def __str__(self):
        return f'{self.name}'
