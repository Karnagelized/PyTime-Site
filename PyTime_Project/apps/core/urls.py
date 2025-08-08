
from django.urls import path
from apps.core.views import (
    MainView, ResumeView, ContactView,
    UserAgreementView, PrivacyView,
    BadRequestView, ForbiddenView, PageNotFoundView,
    InternalServerErrorView, ServiceUnavailableView
)
from PyTime_Project.settings import DEBUG


# Маршруты приложения "core"
urlpatterns = [
    # Основные страницы
    path('', MainView.as_view(), name='mainPage'),
    path('resume', ResumeView.as_view(), name='resumePage'),
    path('contact', ContactView.as_view(), name='contactPage'),
    path('agreement', UserAgreementView.as_view(), name='userAgreement'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
]


if DEBUG:
    urlpatterns += [
        # Страницы ошибок
        path('errors/400', BadRequestView.as_view(), name='badRequest'),
        path('errors/403', ForbiddenView.as_view(), name='forbidden'),
        path('errors/404', PageNotFoundView.as_view(), name='pageNotFound'),
        path('errors/500', InternalServerErrorView.as_view(), name='internalServerError'),
        path('errors/503', ServiceUnavailableView.as_view(), name='serviceUnavailable'),
]

