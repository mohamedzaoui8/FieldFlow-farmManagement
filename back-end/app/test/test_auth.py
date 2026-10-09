from app.core.security import hash_password
from app.database.database import get_db
from app.models.user import User


def add_user(client, email, password ,is_active=True):
    db_override = client.app.dependency_overrides[get_db]
    db = next(db_override())

    user = User(
        name="Test_User",
        email=email,
        password=hash_password(password),
        role="owner",
        is_active=is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ----test_login_valid_credentials----#
def test_login_valid_credentials(client):
    add_user(client, "test@example.com", "testpassword123")

    response = client.post(
        "auth/login", json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


#test_login_non_existent_user
def test_login_non_existent_user(client):
    response = client.post(
        "auth/login", json={"email": "nonexistent@example.com", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "البريد الإلكتروني أو كلمة المرور غير صالحة"

#test_login_invalid_password
def test_login_invalid_password(client):
    add_user(client, "test@example.com", "testpassword123")
    response = client.post(
        "auth/login", json={"email": "test@example.com", "password": "wrongpassword123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "البريد الإلكتروني أو كلمة المرور غير صالحة"

#test_login_inactive_user
def test_login_inactive_user(client):
    add_user(client, "test@example.com", "testpassword123", is_active=False)
    response = client.post(
        "auth/login", json={"email": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "الحساب غير نشط"

#test_get_me_invalid_token
def test_get_me_invalid_token(client):
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401