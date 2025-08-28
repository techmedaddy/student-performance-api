# app/tests/test_students.py

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

def test_create_student():
    response = client.post(
        "/students/",
        json={"name": "John Doe", "age": 20, "department": "Computer Science"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["age"] == 20
    assert data["department"] == "Computer Science"
    assert "id" in data

def test_read_students():
    client.post(
        "/students/",
        json={"name": "Jane Doe", "age": 22, "department": "Physics"},
    )
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Jane Doe"

def test_read_student_by_id():
    create_response = client.post(
        "/students/",
        json={"name": "Jim Beam", "age": 21, "department": "Chemistry"},
    )
    student_id = create_response.json()["id"]
    
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jim Beam"
    assert data["id"] == student_id

    response_not_found = client.get("/students/999")
    assert response_not_found.status_code == 404

def test_search_students_by_name():
    client.post(
        "/students/",
        json={"name": "Alice Smith", "age": 23, "department": "Biology"},
    )
    response = client.get("/students/search/?name=Alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alice Smith"

    response_not_found = client.get("/students/search/?name=Bob")
    assert response_not_found.status_code == 404

def test_delete_student():
    create_response = client.post(
        "/students/",
        json={"name": "To Be Deleted", "age": 25, "department": "History"},
    )
    student_id = create_response.json()["id"]

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Student with id {student_id} deleted successfully."}

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 404
    
    delete_not_found_response = client.delete("/students/999")
    assert delete_not_found_response.status_code == 404
