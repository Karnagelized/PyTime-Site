
from django.urls import path
from core.views import (
    MainView, ResumeView, UserProfileView,
    ArticleAboutView, ArticleListView, ArticlePageView,
    ProjectAboutView, ProjectListView, ProjectPage,
    LoginUserView, LogoutUserView, RegistrationUserView,
    passwordResetEnterMail, passwordResetEnterCode,
    passwordResetEnterNewPassword,
    UserAgreementView, PrivacyView,
    BadRequestView, ForbiddenView, PageNotFoundView,
    InternalServerErrorView, ServiceUnavailableView
)

# Маршруты приложения "core"
urlpatterns = [
    # Основные страницы
    path('', MainView.as_view(), name='mainPage'),
    path('resume', ResumeView.as_view(), name='resumePage'),
    path('profile', UserProfileView.as_view(), name='profilePage'),
    # Статьи
    path('articles', ArticleAboutView.as_view(), name='articlesPage'),
    path('all-articles', ArticleListView.as_view(), name='allArticlesPage'),
    path('articles/article/<slug:articleSlug>', ArticlePageView.as_view(), name='articlePage'),
    # Проекты
    path('projects', ProjectAboutView.as_view(), name='projectsPage'),
    path('all-projects', ProjectListView.as_view(), name='allProjectsPage'),
    path('projects/project/<slug:projectSlug>', ProjectPage.as_view(), name='projectPage'),
    # Аутентификация
    path('login', LoginUserView.as_view(), name='loginUser'),
    path('logout', LogoutUserView.as_view(), name='logoutUser'),
    path('registration', RegistrationUserView.as_view(), name='registrationUser'),
    # path('password-reset', passwordResetEnterMail, name='passwordResetEnterMail'),
    # path('password-reset-enter-code', passwordResetEnterCode, name='passwordResetEnterCode'),
    # path('password-reset-enter-password', passwordResetEnterNewPassword, name='passwordResetEnterNewPassword'),
    # Соглашения
    path('agreement', UserAgreementView.as_view(), name='userAgreement'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
    # Страницы ошибок
    path('errors/400', BadRequestView.as_view(), name='badRequest'),
    path('errors/403', ForbiddenView.as_view(), name='forbidden'),
    path('errors/404', PageNotFoundView.as_view(), name='pageNotFound'),
    path('errors/500', InternalServerErrorView.as_view(), name='internalServerError'),
    path('errors/503', ServiceUnavailableView.as_view(), name='serviceUnavailable'),
]
