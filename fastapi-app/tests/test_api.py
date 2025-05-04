# fastapi-app/tests/test_api.py
import sys
import os
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, save_todos, TodoItem

client = TestClient(app)

def setup_function():
    save_todos([])  # 테스트 전 초기화

def teardown_function():
    save_todos([])  # 테스트 후 정리
    if os.path.exists("todo.json"):
        os.remove("todo.json")
    if os.path.exists("templates/index.html"):
        os.remove("templates/index.html")


def test_get_empty_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_todo():
    todo = {"id": 1, "title": "Test Task", "description": "Testing", "completed": False}
    post_response = client.post("/todos", json=todo)
    assert post_response.status_code == 200

    get_response = client.get("/todos")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    assert get_response.json()[0]["title"] == "Test Task"


def test_delete_todo():
    todo = TodoItem(id=1, title="Delete Me", description="Please", completed=False)
    save_todos([todo.dict()])
    
    delete_response = client.delete("/todos/1")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "To-Do item deleted"

    get_response = client.get("/todos")
    assert get_response.status_code == 200
    assert get_response.json() == []
<<<<<<< HEAD

=======
>>>>>>> 171143f0df3718b39ac246d7a2a2f3d10b453982
