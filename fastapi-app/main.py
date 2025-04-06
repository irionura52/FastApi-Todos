from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI()

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    dueDate: Optional[str] = None
    completed: bool

# JSON 파일 경로
TODO_FILE = "todo.json"

# JSON 파일에서 To-Do 항목 로드
def load_todos():
    if not os.path.exists(TODO_FILE):
        save_todos([])
    try:
        with open(TODO_FILE, "r") as file:
            content = file.read().strip()
            todos = json.loads(content) if content else []

            # 👇 여기서 null → None, 또는 null 제거
            for todo in todos:
                if "dueDate" in todo and todo["dueDate"] is None:
                    # 삭제하거나 기본값 설정 가능
                    todo["dueDate"] = "2099-12-31"  # ← default 날짜 설정
                    # 또는: del todo["dueDate"]  ← 아예 필드 삭제도 가능
            return todos
    except json.JSONDecodeError:
        return []

# JSON 파일에 To-Do 항목 저장
def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)

# To-Do 목록 조회
@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

# 신규 To-Do 항목 추가
@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos = load_todos()
    todos.append(todo.dict())  # 새 항목 추가
    save_todos(todos)
    return todo

# To-Do 항목 수정
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_todo.dict())
            save_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

# To-Do 항목 삭제
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}

# HTML 파일 서빙
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)
