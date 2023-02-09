import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUpdatePasswordView:
    url = reverse('user-update-password')

    def test_user_update_password_success(self, auth_client, faker, user_factory):
        user = user_factory.build()
        response = auth_client.put(self.url, data={
            'old_password': user.password,
            'new_password': faker.password()
        })
        expected_response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_user_update_password_wrong(self, auth_client, faker):
        response = auth_client.put(self.url, data={
            'old_password': 'wrong_password',
            'new_password': faker.password()
        })
        expected_response = {
            'old_password': [
                'Wrong password.'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_user_update_password_same(self, auth_client):
        response = auth_client.put(self.url, data={
            'old_password': 'test_pwd',
            'new_password': 'test_pwd'
        })
        expected_response = {
            'new_password': [
                "Can't be the same."
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_user_update_password_common(self, auth_client):
        response = auth_client.put(self.url, data={
            'old_password': 'test_pwd',
            'new_password': 'Password'
        })
        expected_response = {
            'new_password': [
                'This password is too common.'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_user_update_password_short_numeric(self, auth_client):
        response = auth_client.put(self.url, data={
            'old_password': 'test_pwd',
            'new_password': '1269462'
        })
        expected_response = {
            'new_password': [
                'This password is too short. It must contain at least 8 characters.',
                'This password is entirely numeric.'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response
