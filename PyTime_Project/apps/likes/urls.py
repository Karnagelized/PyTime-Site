
from django.urls import path
from apps.likes.views import ArticleLikeView, ProjectsLikeView


# Маршруты приложения "likes"
urlpatterns = [
    path('like-article/', ArticleLikeView.as_view(), name='likeArticle'),
    path('like-project/', ProjectsLikeView.as_view(), name='likeProject'),
]
