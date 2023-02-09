import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCreateCategoryView:
    url = reverse('category-create')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_create_category(self, auth_client, category_factory, board):
        category = category_factory.create()
        response = auth_client.post(self.url, data={
            'title': category.title,
            'board': board.pk
        }, format='json')

        expected_response = {
            'id': category.pk + 1,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': category.title,
            'is_deleted': category.is_deleted,
            'board': board.pk
        }

        assert response.status_code == 201
        assert response.json() == expected_response

    def test_no_perms_create_board(self, client, category_factory, board):
        goal_category = category_factory.create()
        response = client.post(self.url, data={
            'title': goal_category.title,
            'board': board.pk
        }, format='json')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
