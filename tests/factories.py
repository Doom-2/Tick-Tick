from core.models import User
import factory.fuzzy
from goals.models import (
    Board,
    BoardParticipant,
    GoalCategory,
    Goal,
    GoalComment
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = 'test_pwd'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title: str = factory.fuzzy.FuzzyText(length=10)

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(
                board=self,
                user=owner,
                role=BoardParticipant.Role.owner
            )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title: str = factory.fuzzy.FuzzyText(length=10)
    user: UserFactory = factory.SubFactory(UserFactory)
    board: BoardFactory = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title: str = factory.fuzzy.FuzzyText(length=10)
    user: UserFactory = factory.SubFactory(UserFactory)
    category: CategoryFactory = factory.SubFactory(CategoryFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text: str = factory.fuzzy.FuzzyText(length=10)
    user: UserFactory = factory.SubFactory(UserFactory)
    goal: GoalFactory = factory.SubFactory(GoalFactory)
