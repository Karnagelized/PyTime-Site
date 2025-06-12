
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse
from .models import Article, Project


# Главная страница сайта
def mainPage(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


# Страница с резюме
def resumePage(request: HttpRequest) -> HttpResponse:
    return render(request, 'resume.html')


# Страница описания статей
def articlesPreviewPage(request: HttpRequest) -> HttpResponse:
    lastArticles = Article.published.all().order_by('-datetimeCreate')[:4]

    pageData = {
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
    # ...

    pageData = {
        'articleData': articleData,
    }

    return render(request, 'articles/article_page.html', context=pageData)


# Страница описания проектов
def projectsPreviewPage(request: HttpRequest) -> HttpResponse:
    lastProjects = Project.published.all().order_by('-datetimeCreate')[:4]

    pageData = {
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
    # ...

    pageData = {
        'projectData': projectData,
    }

    return render(request, 'projects/project_page.html', context=pageData)








# Страница с ошибкой 404
def pageNotFound(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'errors/404.html', status=404)
