
from apps.comments.models import Comment
from apps.comments.forms import WriteCommentForm
from django.shortcuts import redirect, reverse
from django.views import View



class ReplyCommentView(View):
    """
        Представление для обработки ответа на комментарий
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        contentType = request.POST.get('commentType')
        contentSlug = request.POST.get('commentSlug')
        commentID = request.POST.get('commentID')

        comment = Comment.objects.get(pk=commentID)
        commentForm = WriteCommentForm(request.POST)

        if not commentForm.is_valid():
            if contentType == 'ARTICLE':
                return redirect(reverse('articlePage', kwargs={'articleSlug': contentSlug}))
            else:
                return redirect(reverse('projectPage', kwargs={'projectSlug': contentSlug}))

        newComment = commentForm.save(commit=False)
        newComment.contentSlug = contentSlug
        newComment.contentType = contentType
        newComment.author = request.user
        newComment.parentComment = comment.parentComment if comment.parentComment else comment
        newComment.toWhomReply = comment.author
        newComment.isReply = True
        newComment.text = commentForm.cleaned_data['content']
        newComment.save()

        if contentType == 'ARTICLE':
            return redirect(reverse('articlePage', kwargs={'articleSlug': contentSlug}))
        else:
            return redirect(reverse('projectPage', kwargs={'projectSlug': contentSlug}))
