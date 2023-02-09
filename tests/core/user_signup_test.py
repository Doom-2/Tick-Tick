import pytest
from django.urls import reverse
from rest_framework import status
from core.models import User
from unittest.mock import ANY


@pytest.mark.django_db
class TestSignUpView:
    url = reverse('create-user')

    def test_user_signup(self, client, user_factory):
        user: User = user_factory.build()
        response = client.post(self.url, data={
            'username': user.username,
            'password': user.password,
            'password_repeat': user.password,
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': ANY,
            'username': user.username,
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ANY
        }
