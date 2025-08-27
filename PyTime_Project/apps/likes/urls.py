
from django.urls import path
from apps.likes.views import (
    ArticleLikeView, ProjectsLikeView, CommentsLikeView, CommentsDislikeView
)


# Маршруты приложения "likes"
urlpatterns = [
    path('like-article/', ArticleLikeView.as_view(), name='likeArticle'),
    path('like-project/', ProjectsLikeView.as_view(), name='likeProject'),
    path('like-comment/', CommentsLikeView.as_view(), name='likeComment'),
    path('dislike-comment/', CommentsDislikeView.as_view(), name='dislikeComment'),
]
