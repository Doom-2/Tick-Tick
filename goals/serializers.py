from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from core.models import User
from core.serializers import UserDetailsSerializer
from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')
        fields = '__all__'

    def create(self, validated_data):
        board_id = self.initial_data.pop('board', None)
        board = get_object_or_404(Board, pk=board_id)

        if not board.participants.filter(user=self.context['request'].user.pk, role__in=[1, 2]).exists():
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        category = GoalCategory.objects.create(**validated_data, board=board)
        return category


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if not value.board.participants.filter(role__in=[1, 2], user=self.context['request'].user):
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_goal(self, value: Goal):
        if value.status == 4:
            raise serializers.ValidationError('not allowed in archived goal')

        if not value.category.board.participants.filter(role__in=[1, 2], user=self.context['request'].user):
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')


''' #################### Board Participant #################### '''


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


''' #################### Board #################### '''


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data: dict):
        owner = validated_data.pop('user')
        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'participants' in validated_data:
            new_participants = validated_data.pop('participants')
            new_by_id = {part['user'].id: part for part in new_participants}

            old_participants = instance.participants.exclude(user=owner)
            with transaction.atomic():
                for old_participant in old_participants:
                    if old_participant.user_id not in new_by_id:
                        old_participant.delete()
                    else:
                        if (
                                old_participant.role
                                != new_by_id[old_participant.user_id]['role']
                        ):
                            old_participant.role = new_by_id[old_participant.user_id][
                                'role'
                            ]
                            old_participant.save()
                        new_by_id.pop(old_participant.user_id)
                for new_part in new_by_id.values():
                    BoardParticipant.objects.create(
                        board=instance, user=new_part['user'], role=new_part['role']
                    )

        instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
