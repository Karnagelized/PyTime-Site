
from django.urls import path
from apps.comments.views import ReplyCommentView


# Маршруты приложения "likes"
urlpatterns = [
    path('reply-comment/', ReplyCommentView.as_view(), name='replyComment'),
]
