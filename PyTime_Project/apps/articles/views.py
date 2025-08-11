
from os import path
from django.urls import reverse
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from apps.articles.models import Article
from apps.comments.models import Comment
from apps.comments.forms import WriteCommentForm
from django.views import View
from PyTime_Project.settings import MEDIA_ROOT


# Представление страницы с информацией о Статьях
class ArticleAboutView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        lastArticles = Article.published.all().order_by('-datetimeCreate')[:4]

        # Проверка на существование изображения Статьи
        for article in lastArticles:
            if not path.exists(MEDIA_ROOT / str(article.image)):
                article.image = ''

        pageData = {
            'title': 'Статьи | PyTime',
            'og_description': 'Анонсы последних статей с кратким описанием и датой публикации.',
            'navigationSelected': 'Articles',
            'lastArticles': lastArticles,
            'lastArticle': lastArticles[0] if len(lastArticles) > 0 else None,
        }

        return render(request, 'articles.html', context=pageData)


# Представление страницы с карточками всех Статей
class ArticleListView(View):
    def post(self, *args, **kwargs) -> HttpResponseNotAllowed:
        return HttpResponseNotAllowed(['GET'])


    def get(self, request:HttpRequest, *args, **kwargs) -> HttpResponse:
        pageData = {
            'title': 'Все статьи | PyTime',
            'og_description': 'Полный каталог статей с фильтрами по темам, датам и популярности.',
            'allArticles': Article.published.all().order_by('-datetimeCreate'),
        }

        return render(request, 'all_articles.html', context=pageData)


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
            pageData['writeCommentForm'] = commentForm
            pageData['comments'] = Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE')

            return render(request, 'article_page.html', context=pageData)

        # Форма не прошла валидацию
        if not commentForm.is_valid():
            pageData['writeCommentForm'] = commentForm

            return render(request, 'project_page.html', context=pageData)

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

        # Добавляем просмотр к статье
        if not request.session.pop('skipViewIncrement', False):
            articleData.increment_views()

        pageData = {
            'articleData': articleData,
            'writeCommentForm': WriteCommentForm(),
            'comments': Comment.getAllByTypeAndSlug(slug=articleSlug, postType='ARTICLE'),
        }

        return render(request, 'article_page.html', context=pageData)
