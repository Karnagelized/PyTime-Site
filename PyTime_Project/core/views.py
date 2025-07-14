
from os import path
from django.urls import reverse
import django.forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, HttpResponse, redirect
from core.models import Article, Project, HardSkillsCategory, CustomUser, Comment
from core.forms import UserLoginForm, UserRegistrationForm, WriteCommentForm
from core.backends import EmailAuthBackend


# Главная страница сайта
def mainPage(request: HttpRequest) -> HttpResponse:
    # Получаем Hard скиллы
    skillsCategory = HardSkillsCategory.visibleCategory.all()

    # Выбор раздела навигации
    pageData = {
        'user': request.user,
        'skillsCategoryData': skillsCategory,
    }

    return render(request, 'index.html', context=pageData)


# Страница с резюме
def resumePage(request: HttpRequest) -> HttpResponse:
    # Получаем Hard скиллы
    skillsCategory = HardSkillsCategory.visibleCategory.all()

    # Выбор раздела навигации
    pageData = {
        'navigationSelected': 'Resume',
        'skillsCategoryData': skillsCategory,
    }

    return render(request, 'resume.html', context=pageData)


# Страница с профилем Пользователя
def profilePage(request: HttpRequest) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_authenticated:
        return redirect('mainPage')

    # Выбор раздела навигации
    pageData = {
        'navigationSelected': 'Profile',
    }

    return render(request, 'profile.html', context=pageData)


# Страница описания статей
def articlesPreviewPage(request: HttpRequest) -> HttpResponse:
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


# Страница со списком всех статей
def allArticlesPreviewPage(request: HttpRequest) -> HttpResponse:
    allArticles = Article.published.all().order_by('-datetimeCreate')

    pageData = {
        'allArticles': allArticles,
    }

    return render(request, 'articles/all_articles.html', context=pageData)


# Страница статьи
def articlePage(request: HttpRequest, articleSlug: int) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()
    articleData = Article.published.filter(slug=articleSlug).first()

    # Проверка на существование
    if articleData is None:
        raise Http404()

    pageData = {
        'articleData': articleData,
        'writeCommentForm': WriteCommentForm(),
        'comments': Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE'),
    }

    if request.POST:
        commentForm = WriteCommentForm(request.POST)

        if user and user.is_authenticated:
            if commentForm.is_valid():
                newComment = commentForm.save(commit=False)
                newComment.contentSlug = articleSlug
                newComment.contentType = 'ARTICLE'
                newComment.author = user
                newComment.text = commentForm.cleaned_data['content']
                newComment.save()

                pageData['comments'] = Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE')

                return redirect(reverse('articlePage', kwargs={'articleSlug': articleSlug}))
            else:
                pageData['writeCommentForm'] = commentForm
        else:
            commentForm.add_error(field=None, error='Пользователь не авторизован!')
            pageData['writeCommentForm'] = commentForm

    return render(request, 'articles/article_page.html', context=pageData)


# Страница описания проектов
def projectsPreviewPage(request: HttpRequest) -> HttpResponse:
    lastProjects = Project.published.all().order_by('-datetimeCreate')[:4]

    # Проверка на существование изображения Статьи
    for project in lastProjects:
        if not path.exists(str(project.image)):
            project.image = ''

    pageData = {
        'navigationSelected': 'Projects',
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
    user = CustomUser.objects.all().filter(id=request.user.id).first()
    projectData = Project.published.filter(slug=projectSlug).first()

    # Проверка на существование
    if projectData is None:
        raise Http404()

    pageData = {
        'projectData': projectData,
        'writeCommentForm': WriteCommentForm(),
        'comments': Comment.getAllByTypeAndSlug(slug=projectSlug, postType='PROJECT'),
    }

    if request.POST:
        commentForm = WriteCommentForm(request.POST)

        if user and user.is_authenticated:
            if commentForm.is_valid():
                newComment = commentForm.save(commit=False)
                newComment.contentSlug = projectSlug
                newComment.contentType = 'PROJECT'
                newComment.author = user
                newComment.text = commentForm.cleaned_data['content']
                newComment.save()

                pageData['comments'] = Comment.getAllByTypeAndSlug(slug=projectSlug, postType='PROJECT')

                return redirect(reverse('projectPage', kwargs={'projectSlug': projectSlug}))
            else:
                pageData['writeCommentForm'] = commentForm
        else:
            commentForm.add_error(field=None, error='Пользователь не авторизован!')
            pageData['writeCommentForm'] = commentForm

    return render(request, 'projects/project_page.html', context=pageData)


# Страница для авторизации Пользователя
def loginUser(request: HttpRequest) -> HttpResponse:
    pageData = {
        'navigationSelected': 'Authorization',
    }

    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)

        if loginForm.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = EmailAuthBackend().authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user=user)
                return redirect('mainPage')

        pageData['loginForm'] = loginForm

        return render(request, 'authentication/authorization.html', context=pageData)
    else:
        pageData['loginForm'] = UserLoginForm()

    return render(request, 'authentication/authorization.html', context=pageData)


# Обработка выхода Пользователя из сессии
def logoutUser(request: HttpRequest) -> HttpResponse:
    isUserAuthenticated = request.user.is_authenticated

    if isUserAuthenticated:
        logout(request)

    return redirect('loginUser')


# Страница для регистрации Пользователя
def registrationUser(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        registrationForm = UserRegistrationForm(request.POST)

        if registrationForm.is_valid():
            # Создаём объект Пользователя без сохранения в БД
            newUser = registrationForm.save(commit=False)
            newUser.set_password(registrationForm.cleaned_data['password'])
            newUser.save()

            return redirect('loginUser')
    else:
        registrationForm = UserRegistrationForm()

    return render(
        request,
        'authentication/registration.html',
        context={
            'registrationForm': registrationForm
        }
    )


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


# Страница Пользовательского соглашения
def userAgreement(request: HttpRequest) -> HttpResponse:
    return render(request, 'agreements/user_agreement.html')


# Страница Политики конфиденциальности
def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, 'agreements/privacy.html')


# Страница с ошибкой 400
def badRequest(request: HttpRequest, exception=None) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_superuser:
        return redirect('mainPage')

    return render(request, 'errors/400.html', status=400)


# Страница с ошибкой 403
def forbidden(request: HttpRequest, exception=None) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_superuser:
        return redirect('mainPage')

    return render(request, 'errors/403.html', status=403)


# Страница с ошибкой 404
def pageNotFound(request: HttpRequest, exception=None) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_superuser:
        return redirect('mainPage')

    return render(request, 'errors/404.html', status=404)


# Страница с ошибкой 500
def internalServerError(request: HttpRequest, exception=None) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_superuser:
        return redirect('mainPage')

    return render(request, 'errors/500.html', status=500)


# Страница с ошибкой 503
def serviceUnavailable(request: HttpRequest, exception=None) -> HttpResponse:
    user = CustomUser.objects.all().filter(id=request.user.id).first()

    if user is None or not user.is_superuser:
        return redirect('mainPage')

    return render(request, 'errors/503.html', status=503)

