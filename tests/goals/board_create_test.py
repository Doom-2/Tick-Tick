import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from freezegun import freeze_time
from goals.models import Board

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestCreateBoardView:
    url = reverse('board-create')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_create_board(self, auth_client, board: Board):
        response = auth_client.post(self.url, data={
            'title': board.title,
        })

        expected_response = {
            'id': 2,
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': board.title,
            'is_deleted': board.is_deleted
        }

        assert response.status_code == 201
        assert response.json() == expected_response

    def test_no_perms_create_board(self, client, board: Board):
        response = client.post(self.url, data={
            'title': board.title,
        })

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
