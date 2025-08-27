
from django.db import models



class VisibleHardSkillsCategoryManager(models.Manager):
    """
        Менеджер для Hard скиллов, который возвращает опубликованные категории
    """

    def get_queryset(self):
        return super().get_queryset().filter(isVisible=True).order_by('position')
