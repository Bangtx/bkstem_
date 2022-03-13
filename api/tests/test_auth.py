from fastapi.testclient import TestClient
from main import app
import json
from config.setting import TOKEN_GENERATION_KEY
from utils import auth, cache


def test_auth_failed_missing_headers():
    """
    Call API without Authentication in headers
    :Expected: return status code 403 Forbidden
    """
    client = TestClient(app)
    response = client.get("/sizes")
    assert response.status_code == 403


def test_auth_failed_missing_token():
    """
    Call API without token
    :Expected: return status code 403 Forbidden
    """
    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer "}
    response = client.get("/sizes")
    assert response.status_code == 403


def test_auth_failed_wrong_format_token():
    """
    Call API with a invalid token
    :Expected: return status code 401 Unauthorized
    """
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqazNNVFUzTVRKQ"
    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/sizes")
    assert response.status_code == 401


def test_auth_failed_invalid_token():
    """
    Call API with a invalid token
    :Expected: return status code 401 Unauthorized
    """
    token = (
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqazNNVFUzTVRKQ"
        "1JFUXlNREJHUkVFeFJEUkJNMFpEUlRBME9USXdRa1pGT1RNNE0wUTNSZyJ9.e"
        "yJpc3MiOiJodHRwczovL290YW5pLWNvcmUuYXV0aDAuY29tLyIsInN1YiI6Im"
        "F1dGgwfDVlMDQ1Y2M5MDdiNzllMGU4NmQxZDEwOSIsImF1ZCI6WyJodHRwczo"
        "vL2Zsb3dlcmJpei5vdGFuaS1zaG9rYWkub3JnIiwiaHR0cHM6Ly9vdGFuaS1j"
        "b3JlLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjA4NzA5ODcsImV4c"
        "CI6MTYyMDg3ODE4NywiYXpwIjoiUHdGZU5EY1p5ZlR5ZUszS2xEZm5LMHR2aF"
        "k3NGZVZW4iLCJzY29wZSI6Im9wZW5pZCJ9.gKMds1JliHkE8ttVSniDOpbwSZ"
        "YmvgrbaTa7wq5pJ0LNcF10HCqC2vrWrxVzrUG093gdyjt4xABt_7wQFTtheIU"
        "_FhJ9aUU04MpRHfm1zVcrtrd4rVZScuC74k-2boaI67dNZAN3EQ8BvKKKguEu"
        "YK84yemWhVbxPKNSGHT6_MzImA6_bohtCmKSpzal-n9uP8zkDy7mpjheDJx6A"
        "1VzZhBK9EN_C5fDUb0SWBzqaRjSncp-loFnNNajHgNCtD2YS_gjKnwj91CFNi"
        "UhuOrj_x0-AL4VGnNDJjr9x4Kmo-9c11J0PtL5Kx7HPhZ1BU_LBJ70j33Uwnl"
        "2Yxu9paha-w"
    )

    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/sizes")
    assert response.status_code == 401


def test_auth_failed_expired_token():
    """
    Call API with a expired token
    :Expected: return status code 401 Unauthorized
    """
    key = json.loads(TOKEN_GENERATION_KEY)
    cache.set("jwks-" + key["kid"], json.dumps(key))
    token = auth.generate_token(key, email="fmbiz@test.com", exp=1622100687)

    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/sizes")
    assert response.status_code == 401


def test_auth_success():
    """
    Call API with a valid token
    :Expected: return status code 200 OK
    """
    key = json.loads(TOKEN_GENERATION_KEY)
    cache.set("jwks-" + key["kid"], json.dumps(key))
    token = auth.generate_token(key, email="fmbiz@test.com")

    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/sizes")
    assert response.status_code == 200
