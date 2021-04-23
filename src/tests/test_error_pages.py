import pytest


@pytest.mark.django_db
def test_404(client):
    response = client.get('/404/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_500(client):
    response = client.get('/404/')
    assert response.status_code == 404
