import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProfileView:
    url = reverse('user-profile')

    def test_user_profile(self, auth_client, user):
        expected_response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        response = auth_client.get(self.url)
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_perms_user_profile(self, client):
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        response = client.get(self.url)
        assert response.status_code == 401
        assert response.json() == expected_response
