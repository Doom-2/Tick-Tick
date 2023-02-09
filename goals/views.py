from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from .filters import GoalDateFilter, CommentFilter, CategoryBoardFilter
from .models import GoalCategory, Goal, GoalComment, Board
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalCreateSerializer,
    GoalSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    BoardCreateSerializer,
    BoardSerializer,
    BoardListSerializer
)
from .permissions import (
    BoardPermissions,
    CategoryPermissions,
    GoalPermissions,
    CommentPermissions
)


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = CategoryBoardFilter
    ordering_fields = ['title', 'created']
    ordering = ['created']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user,
                                           is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        instance.is_deleted = True
        goals = instance.goals.all()
        for goal in goals:
            goal.status = 4
            goal.save()
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['priority', 'due_date']
    ordering = ['-due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        1. Filter categories by their boards where current user is participant
        2. Return goals which are not archived and belong to filtered categories
        :return: <QuerySet>
        """

        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user,
                                                   is_deleted=False)

        return Goal.objects.filter(status__in=[1, 2, 3],
                                   category__in=category_set)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user,
                                                   is_deleted=False)

        return Goal.objects.filter(status__in=[1, 2, 3],
                                   category__in=category_set)

    def perform_destroy(self, instance: Goal):
        instance.status = 4
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = CommentFilter
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user,
                                                   is_deleted=False)
        return GoalComment.objects.filter(goal__category__in=category_set)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user,
                                                   is_deleted=False)
        return GoalComment.objects.filter(goal__category__in=category_set)


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user,
                                    is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)

        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
    ]
    ordering = ['-title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user,
                                    is_deleted=False)
