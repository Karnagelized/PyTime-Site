
from os import path
from typing import Union

from django.urls import reverse
import django.forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from core.models import Article, Project, HardSkillsCategory, CustomUser, Comment
from core.forms import UserLoginForm, UserRegistrationForm, WriteCommentForm
from core.backends import EmailAuthBackend
from django.views import View


# Представление Главной страницы
class MainView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        """Заглушка. POST запроса нет на Главную страницу"""
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'user': request.user,
            'skillsCategoryData': HardSkillsCategory.visibleCategory.all(),
        }

        return render(request, 'index.html', context=pageData)


# Представление страницы с Резюме
class ResumeView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        # Выбор раздела навигации
        pageData = {
            'navigationSelected': 'Resume',
            'skillsCategoryData': HardSkillsCategory.visibleCategory.all(),
        }

        return render(request, 'resume.html', context=pageData)


# Представление страницы Профиля Пользователя
class UserProfileView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_anonymous:
            return redirect('mainPage')

        # Выбор раздела навигации
        pageData = {
            'navigationSelected': 'Profile',
        }

        return render(request, 'profile.html', context=pageData)


# Представление страницы с информацией о Статьях
class ArticleAboutView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        lastArticles = Article.published.all().order_by('-datetimeCreate')[:4]

        # Проверка на существование изображения Статьи
        for article in lastArticles:
            if not path.exists(str(article.image)):
                article.image = ''

        pageData = {
            'navigationSelected': 'Articles',
            'lastArticles': lastArticles,
            'lastArticle': lastArticles[0] if len(lastArticles) > 0 else None,
        }

        return render(request, 'articles/articles.html', context=pageData)


# Представление страницы с карточками всех Статей
class ArticleListView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'allArticles': Article.published.all().order_by('-datetimeCreate'),
        }

        return render(request, 'articles/all_articles.html', context=pageData)


# Представление страницы Статей
class ArticlePageView(View):
    def post(self, request:HttpRequest, articleSlug:str, *args, **kwargs) -> HttpResponse:
        articleData = get_object_or_404(Article, slug=articleSlug)
        commentForm = WriteCommentForm(request.POST)

        pageData = {
            'articleData': articleData,
            'writeCommentForm': WriteCommentForm(),
        }

        # Пользователь не авторизован
        if request.user.is_anonymous:
            commentForm.add_error(field=None, error='Пользователь не авторизован!')
            pageData['writeCommentForm'] = commentForm

            return render(request, 'articles/article_page.html', context=pageData)

        # Сохраняем комментарий
        newComment = commentForm.save(commit=False)
        newComment.contentSlug = articleSlug
        newComment.contentType = 'ARTICLE'
        newComment.author = request.user
        newComment.text = commentForm.cleaned_data['content']
        newComment.save()

        pageData['comments'] = Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE')

        return redirect(reverse('articlePage', kwargs={'articleSlug': articleSlug}))


    def get(self, request:HttpRequest, articleSlug:str, *args, **kwargs) -> HttpResponse:
        articleData = get_object_or_404(Article.published, slug=articleSlug)

        pageData = {
            'articleData': articleData,
            'writeCommentForm': WriteCommentForm(),
            'comments': Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE'),
        }

        return render(request, 'articles/article_page.html', context=pageData)


# Представление страницы с информацией о Проектах
class ProjectAboutView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        lastProjects = Project.published.all().order_by('-datetimeCreate')[:4]

        pageData = {
            'navigationSelected': 'Projects',
            'lastProjects': lastProjects,
            'lastProject': lastProjects[0] if len(lastProjects) > 0 else None,
        }

        return render(request, 'projects/projects.html', context=pageData)


# Представление страницы с карточками всех Проектов
class ProjectListView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'allProjects': Project.published.all().order_by('-datetimeCreate'),
        }

        return render(request, 'projects/all_projects.html', context=pageData)


# Представление страницы Проектов
class ProjectPageView(View):
    def post(self, request:HttpRequest, projectSlug:str, *args, **kwargs) -> HttpResponse:
        projectData = Project.published.filter(slug=projectSlug).first()
        commentForm = WriteCommentForm(request.POST)

        pageData = {
            'projectData': projectData,
            'writeCommentForm': WriteCommentForm(),
        }

        # Пользователь не имеет профиля или не авторизован
        if request.user.is_anonymous:
            commentForm.add_error(field=None, error='Пользователь не авторизован!')
            pageData['writeCommentForm'] = commentForm

            return render(request, 'projects/project_page.html', context=pageData)

        # Форма не прошла валидацию
        if not commentForm.is_valid():
            pageData['writeCommentForm'] = commentForm

            return render(request, 'projects/project_page.html', context=pageData)

        # Сохраняем комментарий
        newComment = commentForm.save(commit=False)
        newComment.contentSlug = projectSlug
        newComment.contentType = 'PROJECT'
        newComment.author = request.user
        newComment.text = commentForm.cleaned_data['content']
        newComment.save()

        pageData['comments'] = Comment.getAllByTypeAndSlug(slug=projectSlug, postType='PROJECT')

        return redirect(reverse('projectPage', kwargs={'projectSlug': projectSlug}))


    def get(self, request:HttpRequest, projectSlug:str, *args, **kwargs) -> HttpResponse:
        projectData = get_object_or_404(Project.published, slug=projectSlug)

        pageData = {
            'projectData': projectData,
            'writeCommentForm': WriteCommentForm(),
            'comments': Comment.getAllByTypeAndSlug(slug=projectSlug, postType='PROJECT'),
        }

        return render(request, 'projects/project_page.html', context=pageData)


# Представление регистрации Пользователя
class RegistrationUserView(View):
    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        registrationForm = UserRegistrationForm(request.POST)

        pageData = {
            'registrationForm': registrationForm,
        }

        # Проверяем валидность формы
        if not registrationForm.is_valid():
            return render(request, 'authentication/registration.html', context=pageData)

        # Создаём объект Пользователя без сохранения в БД
        newUser = registrationForm.save(commit=False)
        newUser.set_password(registrationForm.cleaned_data['password'])
        newUser.save()

        return redirect('loginUser')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('mainPage')

        return render(
            request,
            'authentication/registration.html',
            context={
                'registrationForm': UserRegistrationForm()
            }
        )


# TODO НАПИСАТЬ ТЕСТЫ
# Представление авторизации Пользователя
class LoginUserView(View):
    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'navigationSelected': 'Authorization',
        }

        loginForm = UserLoginForm(request.POST)

        # Проверяем валидность формы
        if not loginForm.is_valid():
            pageData['loginForm'] = loginForm

            return render(request, 'authentication/authorization.html', context=pageData)

        # Получаем данные
        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']

        user = EmailAuthBackend().authenticate(request, email=email, password=password)

        # Аутентификация не прошла
        if not user or not user.is_authenticated:
            pageData['loginForm'] = loginForm

            return render(request, 'authentication/authorization.html', context=pageData)

        # Авторизуем Пользователя
        login(request, user=user)

        return redirect('mainPage')


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('mainPage')

        pageData = {
            'navigationSelected': 'Authorization',
            'loginForm': UserLoginForm(),
        }

        return render(request, 'authentication/authorization.html', context=pageData)


# Представление страницы выхода из профиля Пользователя
class LogoutUserView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            logout(request)

        return redirect('loginUser')


# Страница для восстановления пароля Пользователя - Ввод почты
def passwordResetEnterMail(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'authentication/recovery_password/enter_mail.html')


# Страница для восстановления пароля Пользователя - Ввод кода
def passwordResetEnterCode(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'authentication/recovery_password/confirm_mail_by_code.html')


# Страница для восстановления пароля Пользователя - Ввод нового пароля
def passwordResetEnterNewPassword(request: HttpRequest) -> HttpResponse:
    # Заглушка - В реализации
    return redirect('mainPage')

    return render(request, 'authentication/recovery_password/enter_new_password.html')


# Представление страницы Пользовательского соглашения
class UserAgreementView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'agreements/user_agreement.html')


# Представление страницы Политики конфиденциальности
class PrivacyView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'agreements/privacy.html')


# Представление страницы 400 ошибки - Bad request
class BadRequestView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/400.html', status=400)


# Представление страницы 403 ошибки - Forbidden
class ForbiddenView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/403.html', status=403)


# Представление страницы 404 ошибки - Page not found
class PageNotFoundView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/404.html', status=404)


# Представление страницы 500 ошибки - Internal server error
class InternalServerErrorView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/500.html', status=500)


# Представление страницы 503 ошибки - Service is unavailable
class ServiceUnavailableView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'errors/503.html', status=503)


