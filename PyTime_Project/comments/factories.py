
import factory.django
from comments.models import Comment


# Фабрика для генерации комментариев
class CommentFactory(factory.django.DjangoModelFactory):
    contentSlug = factory.Sequence(lambda n: f"commentSlug_{n}")
    author = factory.SubFactory(UserCustomFactory)

    class Meta:
        model = Comment
