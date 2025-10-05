
from django.http import HttpResponse, Http404, HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from apps.articles.models import Article
from apps.projects.models import Project
from apps.comments.models import Comment
from apps.comments.forms import WriteCommentForm



class ArticleLikeView(View):
    """
        Представление для лайков Статей
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
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



class ProjectsLikeView(View):
    """
        Представление для лайков Проектов
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
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



class CommentsLikeView(View):
    """
        Представление для лайков Комментария
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        contentType = request.POST.get('commentType')
        contentSlug = request.POST.get('commentSlug')
        commentID = request.POST.get('commentID')
        comment = Comment.objects.get(contentType=contentType, pk=commentID)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

        # Удаляем дизлайк, если он есть
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)

        request.session['skipViewIncrement'] = True

        if contentType == 'ARTICLE':
            return redirect(reverse('articlePage', kwargs={'articleSlug': contentSlug}))
        else:
            return redirect(reverse('projectPage', kwargs={'projectSlug': contentSlug}))



class CommentsDislikeView(View):
    """
        Представление для дизлайков Комментария
    """

    def post(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        contentType = request.POST.get('commentType')
        contentSlug = request.POST.get('commentSlug')
        commentID = request.POST.get('commentID')
        comment = Comment.objects.get(contentType=contentType, pk=commentID)

        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
        else:
            comment.dislikes.add(request.user)

        # Удаляем лайк, если он есть
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)

        request.session['skipViewIncrement'] = True

        if contentType == 'ARTICLE':
            return redirect(reverse('articlePage', kwargs={'articleSlug': contentSlug}))
        else:
            return redirect(reverse('projectPage', kwargs={'projectSlug': contentSlug}))
