
from django.urls import path
from core.views import (
    mainPage, resumePage,
    articlesPreviewPage, allArticlesPreviewPage, articlePage,
    projectsPreviewPage, allProjectsPreviewPage, projectPage,
    loginUser, registrationUser, passwordResetEnterMail,
    passwordResetEnterCode, passwordResetEnterNewPassword,
    userAgreement, privacy,
    badRequest, forbidden, pageNotFound, internalServerError
)

# Маршруты приложения "core"
urlpatterns = [
    # Основные страницы
    path('', mainPage, name='mainPage'),
    path('resume', resumePage, name='resumePage'),
    # Статьи
    path('articles', articlesPreviewPage, name='articlesPage'),
    path('all-articles', allArticlesPreviewPage, name='allArticlesPage'),
    path('articles/article/<slug:articleSlug>', articlePage, name='articlePage'),
    # Проекты
    path('projects', projectsPreviewPage, name='projectsPage'),
    path('all-projects', allProjectsPreviewPage, name='allProjectsPage'),
    path('projects/project/<slug:projectSlug>', projectPage, name='projectPage'),
    # Аутентификация
    path('authorization', loginUser, name='authorizationUser'),
    path('registration', registrationUser, name='registrationUser'),
    path('password-reset', passwordResetEnterMail, name='passwordResetEnterMail'),
    path('password-reset', passwordResetEnterCode, name='passwordResetEnterCode'),
    path('password-reset', passwordResetEnterNewPassword, name='passwordResetEnterNewPassword'),
    # Соглашения
    path('agreement', userAgreement, name='userAgreement'),
    path('privacy', privacy, name='privacy'),
    # Страницы ошибок
    path('errors/400', badRequest, name='badRequest'),
    path('errors/403', forbidden, name='forbidden'),
    path('errors/404', pageNotFound, name='pageNotFound'),
    path('errors/500', internalServerError, name='internalServerError'),
]
