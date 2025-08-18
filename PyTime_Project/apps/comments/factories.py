
import factory.django
from factory import fuzzy
from apps.comments.models import Comment
from apps.users.factories import UserCustomFactory
from numpy.random import random_integers


# Фабрика для генерации комментариев
class CommentFactory(factory.django.DjangoModelFactory):
    contentSlug = factory.Sequence(lambda n: f"commentSlug_{n}")
    contentType = fuzzy.FuzzyChoice(choices=[_[0] for _ in Comment.COMMENT_TYPE])
    author = factory.SubFactory(UserCustomFactory)
    toWhomReply = factory.SubFactory(UserCustomFactory)
    isReply = False
    text = ''
    parentComment = None


    @factory.post_generation
    def set_likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.likes.set(extracted)
        else:
            self.likes.set([])


    @factory.post_generation
    def set_dislikes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.dislikes.set(extracted)
        else:
            self.dislikes.set([])


    @factory.post_generation
    def set_parentComment(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.parentComment = extracted
            self.isReply = True

        if self.isReply and not self.parentComment:
            self.parentComment = CommentFactory(isReply=True)
            self.save()


    class Meta:
        model = Comment
