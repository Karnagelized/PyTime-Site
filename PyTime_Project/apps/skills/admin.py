
from django.contrib import admin
from apps.skills.models import HardSkillsCategory, HardSkills



@admin.register(HardSkills)
class HardSkillsAdmin(admin.ModelAdmin):
    """
        Админ модель для Hard скиллов
    """

    view_on_site = False

    list_display = ('name', 'isVisible', 'dateCreate',)
    list_display_links = ('name',)
    list_editable = ('isVisible',)
    ordering = ('name',)



@admin.register(HardSkillsCategory)
class HardSkillsCategoryAdmin(admin.ModelAdmin):
    """
        Админ модель для категорий Hard скиллов
    """

    view_on_site = False

    @admin.display(description='Скиллы')
    def skillsDisplay(self):
        return self.getSkills()

    list_display = ('name', 'position', skillsDisplay, 'isVisible', 'dateCreate',)
    list_display_links = ('name',)
    filter_horizontal = ('skills',)
    list_editable = ('isVisible', 'position',)
    ordering = ('position',)
