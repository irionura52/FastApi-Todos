import os
import pytest
from fastapi.testclient import TestClient
from fastapi_app.main import app, save_todos, load_todos, TodoItem

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # 테스트 전 초기화
    save_todos([])
    yield
    # 테스트 후 정리
    save_todos([])
    if os.path.exists("todo.json"):
        os.remove("todo.json")
    if os.path.exists("templates/index.html"):
        os.remove("templates/index.html")


def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_with_items():
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False)
    save_todos([todo.dict()])
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test"


def test_create_todo():
    todo = {"id": 1, "title": "Test", "description": "Test description", "completed": False}
    response = client.post("/todos", json=todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Test"


def test_create_todo_invalid():
    todo = {"id": 1, "title": "Test"}  # 누락된 필드 있음
    response = client.post("/todos", json=todo)
    assert response.status_code == 422


def test_update_todo():
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False)
    save_todos([todo.dict()])
    updated_todo = {
        "id": 1,
        "title": "Updated",
        "description": "Updated description",
        "completed": True
    }
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_todo_not_found():
    updated_todo = {
        "id": 1,
        "title": "Updated",
        "description": "Updated description",
        "completed": True
    }
    response = client.put("/todos/1", json=updated_todo)
    assert response.status_code == 404


def test_delete_todo():
    todo = TodoItem(id=1, title="Test", description="Test description", completed=False)
    save_todos([todo.dict()])
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "To-Do item deleted"


def test_delete_todo_not_found():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "To-Do item deleted"


def test_read_root():
    os.makedirs("templates", exist_ok=True)
    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write("<h1>Hello from test</h1>")
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello from test" in response.text


def test_load_todos_missing_file():
    if os.path.exists("todo.json"):
        os.remove("todo.json")
    assert load_todos() == []


def test_load_todos_empty_file():
    with open("todo.json", "w") as f:
        f.write("")
    assert load_todos() == []


def test_load_todos_invalid_json():
    with open("todo.json", "w") as f:
        f.write("{ invalid json }")
    assert load_todos() == []
