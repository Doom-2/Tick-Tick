from datetime import date
from django.db import models
from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # for preventing table creation for this model

    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)


class Board(DatesModelMixin):
    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    title = models.CharField(verbose_name='title', max_length=255)
    is_deleted = models.BooleanField(verbose_name='is_deleted', default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    class Role(models.IntegerChoices):
        owner = 1, 'Owner'
        writer = 2, 'Writer'
        reader = 3, 'Reader'

    board = models.ForeignKey(Board, verbose_name='board', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name='role', choices=Role.choices, default=Role.owner)


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    title = models.CharField(verbose_name='title', max_length=255)
    user = models.ForeignKey(User, verbose_name='Author', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='is_deleted', default=False)
    board = models.ForeignKey(Board, verbose_name='board', on_delete=models.PROTECT, related_name='categories')

    def __str__(self):
        return self.title


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'

    class Status(models.IntegerChoices):
        to_do = 1, 'To Do'
        in_progress = 2, 'In progress'
        done = 3, 'Done'
        archived = 4, 'Archived'

    class Priority(models.IntegerChoices):
        low = 1, 'Low'
        medium = 2, 'Medium'
        high = 3, 'High'
        critical = 4, 'Critical'

    title = models.CharField(verbose_name='title', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.PositiveSmallIntegerField(verbose_name='status', choices=Status.choices,
                                              default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='priority', choices=Status.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name='category', on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(verbose_name='deadline', default=date.today, null=True)

    def __str__(self):
        return self.title


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = 'GoalComment'
        verbose_name_plural = 'GoalComments'

    goal = models.ForeignKey(Goal, verbose_name='goal', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='text', max_length=255)
