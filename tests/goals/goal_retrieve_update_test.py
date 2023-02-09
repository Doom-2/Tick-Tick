import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import Goal
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCategoryRetrieveView:
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))
    frozen_date = frozen_datetime[:10]

    def test_goal_retrieve(self, auth_client, board, category, goal_factory, user):
        goal: Goal = goal_factory.create(category=category, user=user)
        url = reverse('goal-retrieve', args=[goal.pk])
        response = auth_client.get(url)
        expected_response = {
            'id': goal.pk,
            'user':
                {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
            'category': category.pk,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': goal.title,
            'description': '',
            'due_date': self.frozen_date,
            'status': goal.status,
            'priority': goal.priority
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_update(self, auth_client, board, category, goal_factory, user):
        goal: Goal = goal_factory.create(category=category, user=user)
        url = reverse('goal-retrieve', args=[goal.pk])
        response = auth_client.patch(url, data={
            'title': 'new_goal_title',
            'description': 'some description',
            'priority': Goal.Priority.high
        }, format='json')
        expected_response = {
            'id': goal.pk,
            'user':
                {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
            'category': category.pk,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': 'new_goal_title',
            'description': 'some description',
            'due_date': self.frozen_date,
            'status': goal.status,
            'priority': Goal.Priority.high
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_perms_goal_retrieve(self, client, board, category, goal_factory, user):
        goal: Goal = goal_factory.create(category=category, user=user)
        url = reverse('goal-retrieve', args=[goal.pk])
        response = client.get(url)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
