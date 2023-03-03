import pytest

pytestmark = pytest.mark.django_db


def test_index_view(client):
    response = client.get("/")
    assert response.status_code == 200
