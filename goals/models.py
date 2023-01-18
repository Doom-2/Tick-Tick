from datetime import date
from django.db import models
from core.models import User


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    title = models.CharField(verbose_name='title', max_length=255)
    user = models.ForeignKey(User, verbose_name='Author', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='is_deleted', default=False)
    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)

    def __str__(self):
        return self.title


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


class Goal(models.Model):
    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'

    title = models.CharField(verbose_name='title', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.PositiveSmallIntegerField(verbose_name='status', choices=Status.choices,
                                              default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='priority', choices=Status.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name='category', on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(verbose_name='deadline', default=date.today, null=True)
    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)

    def __str__(self):
        return self.title


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'GoalComment'
        verbose_name_plural = 'GoalComments'

    goal = models.ForeignKey(Goal, verbose_name='goal', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='text', max_length=255)
    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)
