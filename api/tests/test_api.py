def test_version():
    assert "0.1.0" == "0.1.0"


def test_api(client):
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert data["Hello"] == "test api"
