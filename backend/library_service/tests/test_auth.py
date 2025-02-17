from django.test import Client
import pytest


def authorize(client: Client, username: str, password: str) -> tuple[str, str]:
    response = client.post("/api/auth/login/", {"username": username, "password": password})
    json = response.json()
    return json["access"], json["refresh"]


@pytest.mark.django_db
def test_normal_auth(client: Client):
    access, _ = authorize(client, "user", "1234")

    # Get profile info
    response = client.get("/api/profile/self-info/", headers={"Authorization": f"Bearer {access}"})
    json = response.json()
    assert json == {"username": "user", "first_name": "Alan", "last_name": "Turing", "groups": ["Reader"]}


# TODO: test_bitrix_auth


@pytest.mark.django_db
def test_refresh(client: Client):
    _, refresh = authorize(client, "user", "1234")

    # Refresh the token
    response = client.post("/api/auth/refresh/", {"refresh": refresh})
    json = response.json()
    access: str = json["access"]
    old_refresh = refresh
    refresh: str = json["refresh"]

    # Check that the old refresh token doesn't work
    response = client.post("/api/auth/refresh/", {"refresh": old_refresh})
    assert response.status_code == 401

    # Get profile info with the new token
    response = client.get("/api/profile/self-info/", headers={"Authorization": f"Bearer {access}"})
    json = response.json()
    assert json == {"username": "user", "first_name": "Alan", "last_name": "Turing", "groups": ["Reader"]}


@pytest.mark.django_db
def test_logout(client: Client):
    _, refresh = authorize(client, "user", "1234")

    # Logout
    response = client.post("/api/auth/logout/", {"refresh": refresh})
    assert response.status_code == 200

    # Check that the refresh token doesn't work anymore
    response = client.post("/api/auth/logout/", {"refresh": refresh})
    assert response.status_code == 401
