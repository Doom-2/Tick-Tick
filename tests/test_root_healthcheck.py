import pytest
from django.urls import reverse


def test_root_not_found(client):
    response = client.get('/')

    assert response.status_code == 404


@pytest.mark.django_db()
def test_health_check(client):
    response = client.get(reverse('health-check'))
    assert response.status_code == 200
    assert response.json() == {'status': 'Ok'}
