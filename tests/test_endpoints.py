import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app import models

client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def setup_db():
    # create tables
    Base.metadata.create_all(bind=engine)
    # ensure clean state
    db = SessionLocal()
    db.query(models.Progress).delete()
    db.query(models.Lesson).delete()
    db.query(models.User).delete()
    db.commit()
    db.close()
    yield
    # teardown
    Base.metadata.drop_all(bind=engine)

def test_register_and_login_and_lessons_and_progress():
    # register
    resp = client.post("/auth/register", json={"email":"test@example.com","password":"password123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"
    user_id = data["id"]

    # login
    resp = client.post("/auth/login", json={"email":"test@example.com","password":"password123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    # init lessons via init_data
    import init_data
    init_data  # ensure executed

    # get lessons
    resp = client.get("/lessons/")
    assert resp.status_code == 200
    lessons = resp.json()
    assert len(lessons) >= 1
    lesson_id = lessons[0]["id"]

    # complete lesson
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(f"/progress/complete/{lesson_id}", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "xp" in body
    assert "level" in body
