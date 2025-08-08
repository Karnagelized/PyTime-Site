
from django.db import models


# Менеджер для Hard скиллов, который возвращает опубликованные категории
class VisibleHardSkillsCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isVisible=True).order_by('position')
