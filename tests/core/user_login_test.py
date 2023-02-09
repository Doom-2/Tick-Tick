import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestLoginView:
    url = reverse('login-user')

    def test_user_inactive(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password, is_active=False)
        response = client.post(self.url, data={
            'username': user.username,
            'password': password,
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'non_field_errors': [
                'Account is not activated'
            ]
        }

    def test_invalid_credentials(self, client):
        response = client.post(self.url, data={
            'username': 'wrong_user',
            'password': 'wrong_pwd',
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password)
        response = client.post(self.url, data={
            'username': user.username,
            'password': password,
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'username': user.username,
            'password': user.password
        }
