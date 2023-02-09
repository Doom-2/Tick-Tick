import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.fields import DateTimeField
from unittest.mock import ANY
from core.models import User
from goals.models import Board, BoardParticipant
from tests.factories import UserFactory
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestBoardRetrieveUpdateDeleteView:
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_board_retrieve(self, auth_client, user, board_factory):
        board: Board = board_factory.create(with_owner=user)
        url = reverse('board-retrieve', args=[board.pk])
        response = auth_client.get(url)
        expected_response = {
            'id': board.pk,
            'participants': [
                {
                    'board': board.pk,
                    'created': self.frozen_datetime,
                    'id': ANY,
                    'role': 1,
                    'updated': self.frozen_datetime,
                    'user': user.username
                }
            ],
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': board.title,
            'is_deleted': board.is_deleted,
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_board_update(self, auth_client, user, board_factory):
        board: Board = board_factory.create(with_owner=user)
        new_user: User = UserFactory.create()
        url = reverse('board-retrieve', args=[board.pk])
        response = auth_client.put(url, data={
            'title': 'new_board_title',
            'participants': [
                {
                    'role': BoardParticipant.Role.reader,
                    'user': new_user.username
                }
            ]
        }, format='json')

        expected_response = {
            'id': board.id,
            'participants': [
                {
                    'board': board.pk,
                    'created': self.frozen_datetime,
                    'id': ANY,
                    'role': BoardParticipant.Role.owner,
                    'updated': self.frozen_datetime,
                    'user': user.username
                },
                {
                    'board': board.pk,
                    'created': self.frozen_datetime,
                    'id': ANY,
                    'role': BoardParticipant.Role.reader,
                    'updated': self.frozen_datetime,
                    'user': new_user.username
                }
            ],
            'created': self.frozen_datetime,
            'updated': self.frozen_datetime,
            'title': 'new_board_title',
            'is_deleted': board.is_deleted,
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_board_delete(self, auth_client, board):
        url = reverse('board-retrieve', args=[board.pk])
        response = auth_client.delete(url, content_type='application/json')
        expected_response = None

        assert response.status_code == 204
        assert response.data == expected_response

    def test_no_perms_board_retrieve(self, client, board):
        url = reverse('board-retrieve', args=[board.pk])
        response = client.get(url)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == 401
        assert response.json() == expected_response
