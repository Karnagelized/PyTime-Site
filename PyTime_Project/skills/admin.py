
from django.contrib import admin
from skills.models import HardSkillsCategory, HardSkills


# Админ модель для Hard скиллов
@admin.register(HardSkills)
class HardSkillsAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('name', 'isVisible', 'dateCreate',)
    list_display_links = ('name',)
    list_editable = ('isVisible',)
    ordering = ('name',)


# Админ модель для категорий Hard скиллов
@admin.register(HardSkillsCategory)
class HardSkillsCategoryAdmin(admin.ModelAdmin):
    view_on_site = False

    @admin.display(description='Скиллы')
    def skillsDisplay(self):
        return self.getSkills()

    list_display = ('name', 'position', skillsDisplay, 'isVisible', 'dateCreate',)
    list_display_links = ('name',)
    filter_horizontal = ('skills',)
    list_editable = ('isVisible', 'position',)
    ordering = ('position',)
