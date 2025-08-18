
from django.contrib import admin
from apps.projects.models import Project


# Админ модель для Проектов
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    @admin.display(description="Теги")
    def tagsDisplay(self):
        return ', '.join([f'{tag}' for tag in  self.tags.all()])

    list_display = ('id', 'title', tagsDisplay, 'datetimeCreate', 'datetimeUpdate', 'isPublished',)
    list_display_links = ('title',)
    filter_horizontal = ('tags',)
    list_editable = ('isPublished',)
    ordering = ('-datetimeCreate',)


    def view_on_site(self, obj):
        return obj.get_absolute_url()


    class Media:
        css = {
            'all': ('core/css/custom_ckeditor_admin.css',)
        }
