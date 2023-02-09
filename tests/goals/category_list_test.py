import pytest
from datetime import datetime
from typing import List
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import GoalCategory
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCategoryListView:
    url = reverse('category-list')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_category_list(self, auth_client, board, user, category_factory):
        categories: List[GoalCategory] = category_factory.create_batch(2, board=board, user=user)

        response = auth_client.get(self.url)
        expected_response = [
            {
                'id': categories[0].pk,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': categories[0].title,
                'is_deleted': categories[0].is_deleted,
                'board': board.pk
            },
            {
                'id': categories[1].pk,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': categories[1].title,
                'is_deleted': categories[1].is_deleted,
                'board': board.pk
            }
        ]

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_perms_category_list(self, client, board, user, category_factory):
        category_factory.create_batch(2, board=board, user=user)
        response = client.get(self.url)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
