from test_auth import add_user

from app.database.database import get_db
from app.models.user import User


def get_owner_token(client):
    add_user(client, "owner@example.com", "ownerpassword123")
    response = client.post(
        "auth/login", json={"email": "owner@example.com", "password": "ownerpassword123"}
    )
    return response.json()["access_token"]

#test_create_user_chef
def test_create_user_chef(client):
    token = get_owner_token(client)
    response = client.post(
        "/users/",
        json={"name": "Chef User", "email": "chef@example.com", "password": "chefpassword123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "تم إنشاء المشرف بنجاح"

#test_existing_email_chef_create
def test_existing_email_chef_create(client):
    token = get_owner_token(client)
    add_user(client, "chef@example.com", "chefpassword123")
    response = client.post(
        "/users/",
        json={"name": "Another Chef", "email": "chef@example.com", "password": "anotherchefpassword123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "البريد الإلكتروني مسجل مسبقاً"

#test_read_all_chefs
def test_read_all_chefs(client):
    token = get_owner_token(client)
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200