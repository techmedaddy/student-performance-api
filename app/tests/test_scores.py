# app/tests/test_scores.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_add_or_update_score():
    student_res = client.post("/students/", json={"name": "Alice", "age": 21, "department": "Physics"})
    student_id = student_res.json()["id"]

    add_score_res = client.post(
        f"/students/{student_id}/scores/",
        json={"subject": "Quantum Mechanics", "score": 95.5}
    )
    assert add_score_res.status_code == 201
    data = add_score_res.json()
    assert data["subject"] == "Quantum Mechanics"
    assert data["score"] == 95.5
    assert data["student_id"] == student_id

    update_score_res = client.post(
        f"/students/{student_id}/scores/",
        json={"subject": "Quantum Mechanics", "score": 98.0}
    )
    assert update_score_res.status_code == 201
    updated_data = update_score_res.json()
    assert updated_data["score"] == 98.0

def test_get_student_average_score():
    student_res = client.post("/students/", json={"name": "Bob", "age": 22, "department": "Chemistry"})
    student_id = student_res.json()["id"]

    client.post(f"/students/{student_id}/scores/", json={"subject": "Organic Chemistry", "score": 88})
    client.post(f"/students/{student_id}/scores/", json={"subject": "Physical Chemistry", "score": 92})

    avg_res = client.get(f"/students/{student_id}/average-score/")
    assert avg_res.status_code == 200
    assert avg_res.json() == {"student_id": student_id, "average_score": 90.0}
    
    avg_res_404 = client.get("/students/999/average-score/")
    assert avg_res_404.status_code == 404

def test_get_top_scorer_in_subject():
    student1_res = client.post("/students/", json={"name": "Charlie", "age": 20, "department": "History"})
    student1_id = student1_res.json()["id"]
    client.post(f"/students/{student1_id}/scores/", json={"subject": "World History", "score": 92})

    student2_res = client.post("/students/", json={"name": "Diana", "age": 21, "department": "History"})
    student2_id = student2_res.json()["id"]
    client.post(f"/students/{student2_id}/scores/", json={"subject": "World History", "score": 95})

    top_scorer_res = client.get("/students/top-scorer/World History/")
    assert top_scorer_res.status_code == 200
    data = top_scorer_res.json()
    assert data["name"] == "Diana"
    assert data["student_id"] == student2_id
    assert data["score"] == 95

    top_scorer_404 = client.get("/students/top-scorer/Ancient Mythology/")
    assert top_scorer_404.status_code == 404

def test_get_department_average_score():
    eng_student1_res = client.post("/students/", json={"name": "Eve", "age": 22, "department": "Engineering"})
    eng_student1_id = eng_student1_res.json()["id"]
    client.post(f"/students/{eng_student1_id}/scores/", json={"subject": "Thermodynamics", "score": 80})

    eng_student2_res = client.post("/students/", json={"name": "Frank", "age": 23, "department": "Engineering"})
    eng_student2_id = eng_student2_res.json()["id"]
    client.post(f"/students/{eng_student2_id}/scores/", json={"subject": "Statics", "score": 90})

    art_student_res = client.post("/students/", json={"name": "Grace", "age": 20, "department": "Arts"})
    art_student_id = art_student_res.json()["id"]
    client.post(f"/students/{art_student_id}/scores/", json={"subject": "Sculpture", "score": 98})

    dept_avg_res = client.get("/departments/Engineering/average-score/")
    assert dept_avg_res.status_code == 200
    assert dept_avg_res.json() == {"department": "Engineering", "average_score": 85.0}

    dept_avg_404 = client.get("/departments/Medicine/average-score/")
    assert dept_avg_404.status_code == 404
