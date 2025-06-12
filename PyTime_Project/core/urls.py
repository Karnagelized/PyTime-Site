
from django.urls import path
from core.views import (
    mainPage, resumePage,
    articlesPreviewPage, allArticlesPreviewPage, articlePage,
    projectsPreviewPage, allProjectsPreviewPage, projectPage,
    pageNotFound
)

# Маршруты приложения "core"
urlpatterns = [
    path('', mainPage, name='mainPage'),
    path('resume', resumePage, name='resumePage'),
    # Статьи
    path('articles', articlesPreviewPage, name='articlesPage'),
    path('all-articles', allArticlesPreviewPage, name='allArticlesPage'),
    path('articles/article/<slug:articleSlug>', articlePage, name='articlePage'),
    # Проекты
    path('projects', projectsPreviewPage, name='projectsPage'),
    path('all-projects', allProjectsPreviewPage, name='allProjectsPage'),
    path('articles/project/<slug:projectSlug>', projectPage, name='projectPage'),
    # Страницы ошибок
    path('errors/404', pageNotFound, name='pageNotFound'),
]
