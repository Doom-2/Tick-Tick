from rest_framework import serializers
from core.serializers import UserDetailsSerializer
from .models import GoalCategory, Goal, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

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
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')
