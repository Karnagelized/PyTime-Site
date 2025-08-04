
from django.urls import path
from articles.views import ArticleAboutView, ArticleListView, ArticlePageView


# Маршруты приложения "articles"
urlpatterns = [
    path('articles', ArticleAboutView.as_view(), name='articlesPage'),
    path('all-articles', ArticleListView.as_view(), name='allArticlesPage'),
    path('articles/article/<slug:articleSlug>', ArticlePageView.as_view(), name='articlePage'),
]
