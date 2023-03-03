import pytest

pytestmark = pytest.mark.django_db


def test_get(client):
    response = client.get("/robots.txt")
    request = response.wsgi_request
    content = response.content.decode()
    user_agent_directive = "User-Agent: *"
    sitemap_directive = f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml"
    assert response.status_code == 200
    assert response["content-type"] == "text/plain"
    assert user_agent_directive in content
    assert sitemap_directive in content
