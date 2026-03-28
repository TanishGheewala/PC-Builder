from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = ROOT / "backend" / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

import app.models.category  # noqa: E402,F401
import app.models.transaction  # noqa: E402,F401
import app.models.user  # noqa: E402,F401
import app.routes.auth as auth_routes  # noqa: E402
import app.routes.user as user_routes  # noqa: E402
from app.core.database import Base  # noqa: E402
from backend.main import app  # noqa: E402


def _register_user(client: TestClient):
    return client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test.user@example.com",
            "password": "test1234",
        },
    )


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_auth_users.db"
    test_engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    monkeypatch.setattr(auth_routes, "SessionLocal", testing_session_local)
    monkeypatch.setattr(user_routes, "SessionLocal", testing_session_local)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_register_user(client: TestClient):
    response = _register_user(client)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Test User"
    assert body["email"] == "test.user@example.com"
    assert "id" in body
    assert "created_at" in body


def test_duplicate_registration_returns_409(client: TestClient):
    first = _register_user(client)
    second = _register_user(client)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "Email already registered"


def test_login_and_read_me(client: TestClient):
    _register_user(client)

    login_response = client.post(
        "/auth/login",
        json={
            "email": "test.user@example.com",
            "password": "test1234",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "test.user@example.com"


def test_user_crud_flow(client: TestClient):
    register_response = _register_user(client)
    user_id = register_response.json()["id"]

    list_response = client.get("/users/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == user_id

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Updated User",
            "email": "updated.user@example.com",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated User"

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/users/{user_id}")
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "User not found"


def test_login_with_wrong_password_returns_401(client: TestClient):
    _register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": "test.user@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_read_me_without_token_returns_401(client: TestClient):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing or invalid authorization header"
