
from django.contrib import admin
from apps.tags.models import Tag



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
        Админ модель для Тегов статей и проектов
    """

    list_display = ('id', 'name', 'datetimeCreate', 'datetimeUpdate',)
    list_display_links = ('name',)
    ordering = ('-datetimeCreate',)
