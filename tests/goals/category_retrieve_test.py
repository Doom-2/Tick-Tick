import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import GoalCategory
from tests.factories import CategoryFactory
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCategoryRetrieveView:
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_category_retrieve(self, auth_client, user, board):
        category: GoalCategory = CategoryFactory.create(board=board, user=user)
        url = reverse('category-retrieve', args=[category.pk])
        response = auth_client.get(url)
        expected_response = {
                'id': category.id,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                },
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': category.title,
                'is_deleted': category.is_deleted,
                'board': board.pk
            }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_perms_category_retrieve(self, client, board, category):
        url = reverse('category-retrieve', args=[category.pk])
        response = client.get(url)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
