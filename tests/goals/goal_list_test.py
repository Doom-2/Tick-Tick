import pytest
from datetime import datetime
from typing import List
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import Goal
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestGoalListView:
    url = reverse('goal-list')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))
    frozen_date = frozen_datetime[:10]

    def test_goal_list(self, auth_client, board, category, goal_factory, user):
        goals: List[Goal] = goal_factory.create_batch(2, category=category, user=user)

        response = auth_client.get(self.url)
        expected_response = [
            {
                'id': goals[0].pk,
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
                'title': goals[0].title,
                'description': '',
                'due_date': self.frozen_date,
                'status': goals[0].status,
                'priority': goals[0].priority

            },
            {
                'id': goals[1].pk,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'category': category.pk,
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': goals[1].title,
                'description': '',
                'due_date': self.frozen_date,
                'status': goals[1].status,
                'priority': goals[1].priority

            }
        ]

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_perms_goal_list(self, client, board, category, goal_factory, user):
        goal_factory.create_batch(2, category=category, user=user)

        response = client.get(self.url)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
