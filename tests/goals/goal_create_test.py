import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import GoalCategory
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCreateGoalView:
    url = reverse('goal-create')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))
    frozen_date = frozen_datetime[:10]

    def test_create_goal(self, auth_client, board, category, goal):
        response = auth_client.post(self.url, data={
            'title': goal.title,
            'category': category.pk
        }, format='json')

        expected_response = {
            'id': goal.pk + 1,
            'category': category.pk,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': goal.title,
            'description': '',
            'due_date': self.frozen_date,
            'status': goal.status,
            'priority': goal.priority

        }

        assert response.status_code == 201
        assert response.json() == expected_response

    def test_not_allowed_create_goal(self, auth_client, board, category_factory, goal):
        category: GoalCategory = category_factory.create(is_deleted=True)
        response = auth_client.post(self.url, data={
            'title': goal.title,
            'category': category.pk
        }, format='json')

        expected_response = {
            'category': [
                'not allowed in deleted category'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_no_perms_create_goal(self, client, board, category, goal):
        response = client.post(self.url, data={
            'title': goal.title,
            'category': category.pk
        }, format='json')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
