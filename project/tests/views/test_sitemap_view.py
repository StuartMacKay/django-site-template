import pytest

pytestmark = pytest.mark.django_db


def test_get(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
