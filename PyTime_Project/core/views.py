
from os import path
from django.http import HttpRequest, Http404
from django.shortcuts import render, HttpResponse
from .models import Article, Project


"""
    Основные страницы 
"""

# Главная страница сайта
def mainPage(request: HttpRequest) -> HttpResponse:
    # Выбор раздела навигации
    pageData = {
        'navigationSelected': 0,
    }

    return render(request, 'index.html', context=pageData)


# Страница с резюме
def resumePage(request: HttpRequest) -> HttpResponse:
    # Выбор раздела навигации
    pageData = {
        'navigationSelected': 3,
    }

    return render(request, 'resume.html', context=pageData)


def profilePage(request: HttpRequest) -> HttpResponse:
    return render(request, 'profile.html')


"""
    Страницы для раздела со Статьями 
"""

# Страница описания статей
def articlesPreviewPage(request: HttpRequest) -> HttpResponse:
    lastArticles = Article.published.all().order_by('-datetimeCreate')[:4]

    # Проверка на существование изображения Статьи
    for article in lastArticles:
        if not path.exists(str(article.image)):
            article.image = ''

    pageData = {
        'navigationSelected': 2,
        'lastArticles': lastArticles,
        'lastArticle': lastArticles[0] if len(lastArticles) > 0 else None,
    }

    return render(request, 'articles/articles.html', context=pageData)


# Страница со списком всех статей
def allArticlesPreviewPage(request: HttpRequest) -> HttpResponse:
    allArticles = Article.published.all().order_by('-datetimeCreate')

    pageData = {
        'allArticles': allArticles,
    }

    return render(request, 'articles/all_articles.html', context=pageData)


# Страница статьи
def articlePage(request: HttpRequest, articleSlug: int) -> HttpResponse:
    articleData = Article.published.filter(slug=articleSlug).first()

    # Проверка на существование
    if articleData is None:
        raise Http404()

    pageData = {
        'articleData': articleData,
    }

    return render(request, 'articles/article_page.html', context=pageData)


"""
    Страницы для раздела с Проектами 
"""

# Страница описания проектов
def projectsPreviewPage(request: HttpRequest) -> HttpResponse:
    lastProjects = Project.published.all().order_by('-datetimeCreate')[:4]

    # Проверка на существование изображения Статьи
    for project in lastProjects:
        if not path.exists(str(project.image)):
            project.image = ''

    pageData = {
        'navigationSelected': 1,
        'lastProjects': lastProjects,
        'lastProject': lastProjects[0] if len(lastProjects) > 0 else None,
    }

    return render(request, 'projects/projects.html', context=pageData)


# Страница со списком всех статей
def allProjectsPreviewPage(request: HttpRequest) -> HttpResponse:
    allProjects = Project.published.all().order_by('-datetimeCreate')

    pageData = {
        'allProjects': allProjects,
    }

    return render(request, 'projects/all_projects.html', context=pageData)


# Страница статьи
def projectPage(request: HttpRequest, projectSlug: int) -> HttpResponse:
    projectData = Project.published.filter(slug=projectSlug).first()

    # Проверка на существование
    if projectData is None:
        raise Http404()

    pageData = {
        'projectData': projectData,
    }

    return render(request, 'projects/project_page.html', context=pageData)


"""
    Страницы аутентификации Пользователя 
"""

# Страница для авторизации Пользователя
def loginUser(request: HttpRequest) -> HttpResponse:
    return render(request, 'authentication/authorization.html')


# Страница для регистрации Пользователя
def registrationUser(request: HttpRequest) -> HttpResponse:
    return render(request, 'authentication/registration.html')


# Страница для восстановления пароля Пользователя - Ввод почты
def passwordResetEnterMail(request: HttpRequest) -> HttpResponse:
    return render(request, 'recovery_password/enter_mail.html')


# Страница для восстановления пароля Пользователя - Ввод кода
def passwordResetEnterCode(request: HttpRequest) -> HttpResponse:
    return render(request, 'recovery_password/confirm_mail_by_code.html')


# Страница для восстановления пароля Пользователя - Ввод нового пароля
def passwordResetEnterNewPassword(request: HttpRequest) -> HttpResponse:
    return render(request, 'recovery_password/enter_new_password.html')











"""
    Страницы Пользовательского соглашения и Политики конфиденциальности 
"""

# Страница Пользовательского соглашения
def userAgreement(request: HttpRequest) -> HttpResponse:
    return render(request, 'agreements/user_agreement.html')


# Страница Политики конфиденциальности
def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, 'agreements/privacy.html')


"""
    Страницы для переопределения ошибок 400, 403, 404, 500 
"""

# Страница с ошибкой 400
def badRequest(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'errors/400.html', status=400)

# Страница с ошибкой 403
def forbidden(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'errors/403.html', status=403)

# Страница с ошибкой 404
def pageNotFound(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'errors/404.html', status=404)

# Страница с ошибкой 500
def internalServerError(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'errors/500.html', status=500)

