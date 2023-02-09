import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import Goal, GoalComment
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCreateCommentView:
    url = reverse('comment-create')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_create_comment(self, auth_client, board, category, goal, comment_factory):
        comment: GoalComment = comment_factory.create()
        response = auth_client.post(self.url, data={
            'text': comment.text,
            'goal': goal.pk
        }, format='json')

        expected_response = {
            'id': comment.pk + 1,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'text': comment.text,
            'goal': goal.pk,
        }

        assert response.status_code == 201
        assert response.json() == expected_response

    def test_not_allowed_create_comment(self, auth_client, goal_factory, comment_factory):
        goal: Goal = goal_factory.create(status=Goal.Status.archived)
        comment: GoalComment = comment_factory.create()
        response = auth_client.post(self.url, data={
            'text': comment.text,
            'goal': goal.pk
        }, format='json')

        expected_response = {
            'goal': [
                'not allowed in archived goal'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_no_perms_create_comment(self, client, board, category, goal, comment_factory):
        comment: GoalComment = comment_factory.create()
        response = client.post(self.url, data={
            'text': comment.text,
            'goal': goal.pk
        }, format='json')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
