
from django.contrib import admin
from tags.models import Tag


# Админ модель для тегов Статей и Проектов
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'datetimeCreate', 'datetimeUpdate',)
    list_display_links = ('name',)
    ordering = ('-datetimeCreate',)
