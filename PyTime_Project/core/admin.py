
from django.contrib import admin
from .models import Tag, Article, Project


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'datetimeCreate', 'datetimeUpdate',)
    list_display_links = ('name',)
    ordering = ('-datetimeCreate',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    @admin.display(description="tags")
    def tagsDisplay(self):
        return ', '.join([f'{tag}' for tag in  self.tags.all()])

    list_display = ('id', 'title', tagsDisplay, 'datetimeCreate', 'datetimeUpdate', 'isPublished')
    list_display_links = ('title',)
    filter_horizontal = ('tags',)
    list_editable = ('isPublished',)
    ordering = ('-datetimeCreate',)


    def view_on_site(self, obj):
        return obj.get_absolute_url()

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    @admin.display(description="tags")
    def tagsDisplay(self):
        return ', '.join([f'{tag}' for tag in  self.tags.all()])

    list_display = ('id', 'title', tagsDisplay, 'datetimeCreate', 'datetimeUpdate', 'isPublished')
    list_display_links = ('title',)
    filter_horizontal = ('tags',)
    list_editable = ('isPublished',)
    ordering = ('-datetimeCreate',)


    def view_on_site(self, obj):
        return obj.get_absolute_url()

