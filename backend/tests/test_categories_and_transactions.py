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
import app.routes.category as category_routes  # noqa: E402
import app.routes.transaction as transaction_routes  # noqa: E402
import app.routes.user as user_routes  # noqa: E402
from app.core.database import Base  # noqa: E402
from backend.main import app  # noqa: E402


def _register_user(client: TestClient):
    return client.post(
        "/auth/register",
        json={
            "name": "Category User",
            "email": "category.user@example.com",
            "password": "test1234",
        },
    )


def _create_category(client: TestClient, user_id: int):
    return client.post(
        "/categories/",
        json={
            "name": "GPU",
            "user_id": user_id,
        },
    )


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_categories_transactions.db"
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

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[category_routes.get_db] = override_get_db
    app.dependency_overrides[transaction_routes.get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_category_crud_flow(client: TestClient):
    user_response = _register_user(client)
    user_id = user_response.json()["id"]

    create_response = _create_category(client, user_id)
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    list_response = client.get("/categories/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "GPU"

    update_response = client.put(
        f"/categories/{category_id}",
        json={"name": "CPU"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "CPU"

    delete_response = client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/categories/{category_id}")
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Category not found"


def test_transaction_crud_flow(client: TestClient):
    user_response = _register_user(client)
    user_id = user_response.json()["id"]

    category_response = _create_category(client, user_id)
    category_id = category_response.json()["id"]

    create_response = client.post(
        "/transactions/",
        json={
            "amount": 499.99,
            "description": "Graphics card purchase",
            "user_id": user_id,
            "category_id": category_id,
        },
    )
    assert create_response.status_code == 201
    transaction_id = create_response.json()["id"]

    list_response = client.get("/transactions/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/transactions/{transaction_id}")
    assert get_response.status_code == 200
    assert get_response.json()["amount"] == 499.99

    update_response = client.put(
        f"/transactions/{transaction_id}",
        json={
            "amount": 549.99,
            "description": "Updated graphics card purchase",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 549.99

    delete_response = client.delete(f"/transactions/{transaction_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/transactions/{transaction_id}")
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Transaction not found"
