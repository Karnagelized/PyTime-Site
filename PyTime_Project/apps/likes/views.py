
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from apps.articles.models import Article
from apps.projects.models import Project


# Представление для лайков Статей
class ArticleLikeView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        slug = request.POST.get('contentSlug')
        parentURL = request.POST.get('parentURL')
        article = get_object_or_404(Article, slug=slug)

        # Не авторизованным Пользователям запрещено ставить лайки
        if not user or not user.is_authenticated:
            request.session['skipViewIncrement'] = True

            return redirect(
                parentURL,
                data={'articleSlug': slug, 'isFromLike': True},
            )

        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
        else:
            article.likes.add(user)

        article.save()
        request.session['skipViewIncrement'] = True

        return redirect(parentURL, kwargs={'isFromLike': True})


# Представление для лайков Проектов
class ProjectsLikeView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        slug = request.POST.get('contentSlug')
        parentURL = request.POST.get('parentURL')
        project = get_object_or_404(Project, slug=slug)

        # Не авторизованным Пользователям запрещено ставить лайки
        if not user or not user.is_authenticated:
            request.session['skipViewIncrement'] = True

            return redirect(
                parentURL,
                data={'projectSlug': slug, 'isFromLike': True},
            )

        if project.likes.filter(id=user.id).exists():
            project.likes.remove(user)
        else:
            project.likes.add(user)

        project.save()
        request.session['skipViewIncrement'] = True

        return redirect(parentURL, kwargs={'isFromLike': True})
