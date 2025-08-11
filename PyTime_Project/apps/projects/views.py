
from django.urls import reverse
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from apps.projects.models import Project
from apps.comments.models import Comment
from apps.comments.forms import WriteCommentForm
from django.views import View


# Представление страницы с информацией о Проектах
class ProjectAboutView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        lastProjects = Project.published.all().order_by('-datetimeCreate')[:4]

        pageData = {
            'title': 'Проекты Разработчика | PyTime',
            'og_description': 'Подборка актуальных проектов с кратким описанием и технологиями.',
            'navigationSelected': 'Projects',
            'lastProjects': lastProjects,
            'lastProject': lastProjects[0] if len(lastProjects) > 0 else None,
        }

        return render(request, 'projects.html', context=pageData)


# Представление страницы с карточками всех Проектов
class ProjectListView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Все проекты | PyTime',
            'og_description': 'Архив завершенных и текущих проектов с возможностью сортировки.',
            'allProjects': Project.published.all().order_by('-datetimeCreate'),
        }

        return render(request, 'all_projects.html', context=pageData)


# Представление страницы Проектов
class ProjectPageView(View):
    def post(self, request:HttpRequest, projectSlug:str, *args, **kwargs) -> HttpResponse:
        projectData = get_object_or_404(Project, slug=projectSlug)
        commentForm = WriteCommentForm(request.POST)

        pageData = {
            'projectData': projectData,
            'writeCommentForm': WriteCommentForm(),
        }

        # Пользователь не авторизован
        if request.user.is_anonymous:
            pageData['writeCommentForm'] = commentForm
            pageData['comments'] = Comment.getAllByTypeAndSlug(slug=articleSlug, postType='PROJECT')

            return render(request, 'project_page.html', context=pageData)

        # Форма не прошла валидацию
        if not commentForm.is_valid():
            pageData['writeCommentForm'] = commentForm

            return render(request, 'project_page.html', context=pageData)

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

        # Добавляем просмотр к статье
        if not request.session.pop('skipViewIncrement', False):
            projectData.increment_views()

        pageData = {
            'projectData': projectData,
            'writeCommentForm': WriteCommentForm(),
            'comments': Comment.getAllByTypeAndSlug(slug=projectSlug, postType='PROJECT'),
        }

        return render(request, 'project_page.html', context=pageData)
