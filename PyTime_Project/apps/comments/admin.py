
from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
        Админ модель для Комментариев
    """

    view_on_site = False

    list_display = (
        'id', 'contentSlug', 'contentType', 'author', 'text', 'isReply', 'isVisible', 'dateCreate',
    )
    list_editable = ('isVisible',)
    ordering = ('-dateCreate',)
