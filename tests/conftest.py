import pytest
from pytest_factoryboy import register
from goals.models import Board, GoalCategory, Goal
from tests.factories import (
    UserFactory,
    BoardFactory,
    CategoryFactory,
    GoalFactory,
    CommentFactory
)

pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(BoardFactory)
register(CategoryFactory)
register(GoalFactory)
register(CommentFactory)


@pytest.fixture()
def board(user) -> Board:
    return BoardFactory.create(with_owner=user)


@pytest.fixture()
def category(user, board) -> GoalCategory:
    return CategoryFactory.create(board=board, user=user)


@pytest.fixture()
def goal(user, board, category) -> Goal:
    return GoalFactory.create(category=category, user=user)
