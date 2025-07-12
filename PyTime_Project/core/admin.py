
from django.contrib import admin
from .models import Tag, Article, Project
from .models import (
    Tag, Article, Project, HardSkillsCategory, HardSkills
)


# Админ модель для тегов Статей и Проектов
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'datetimeCreate', 'datetimeUpdate', )
    list_display_links = ('name', )
    ordering = ('-datetimeCreate', )


# Админ модель для Статей
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    @admin.display(description="Теги")
    def tagsDisplay(self):
        return ', '.join([f'{tag}' for tag in  self.tags.all()])

    list_display = ('id', 'title', tagsDisplay, 'datetimeCreate', 'datetimeUpdate', 'isPublished', )
    list_display_links = ('title', )
    filter_horizontal = ('tags', )
    list_editable = ('isPublished', )
    ordering = ('-datetimeCreate', )

    def view_on_site(self, obj):
        return obj.get_absolute_url()


# Админ модель для Проектов
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    @admin.display(description="Теги")
    def tagsDisplay(self):
        return ', '.join([f'{tag}' for tag in  self.tags.all()])

    list_display = ('id', 'title', tagsDisplay, 'datetimeCreate', 'datetimeUpdate', 'isPublished', )
    list_display_links = ('title', )
    filter_horizontal = ('tags', )
    list_editable = ('isPublished', )
    ordering = ('-datetimeCreate', )

    def view_on_site(self, obj):
        return obj.get_absolute_url()


# Админ модель для Hard скиллов
@admin.register(HardSkills)
class HardSkillsAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('name', 'isVisible', 'dateCreate', )
    list_display_links = ('name', )
    list_editable = ('isVisible', )
    ordering = ('name', )


# Админ модель для категорий Hard скиллов
@admin.register(HardSkillsCategory)
class HardSkillsCategoryAdmin(admin.ModelAdmin):
    view_on_site = False

    @admin.display(description='Скиллы')
    def skillsDisplay(self):
        return self.getSkills()

    list_display = ('name', 'position', skillsDisplay, 'isVisible', 'dateCreate', )
    list_display_links = ('name', )
    filter_horizontal = ('skills', )
    list_editable = ('isVisible', 'position', )
    ordering = ('position', 'name', )




