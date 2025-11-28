from database import JsonDatabase
from pathlib import Path
from models import User, TodoItem
from datetime import datetime

class TodoService:
    db: JsonDatabase

    def __init__(self):
        pass

    def create_todo(self, user_id: int, title: str) -> TodoItem:
        if user_id not in ([user.id for user in self.db.users]):
            raise Exception(f"User {user_id} does not exist")
        todo = TodoItem(
            user_id=user_id,
            title=title,
            completed=False,
            created_at=datetime.today())
        self.db.todos.append(todo)
        self.db.save_todos()
        return todo
    
    def list_todos(self, user_id: int, title: str) -> list[TodoItem]:
        return [todo for todo in self.db.todos if todo.user_id == user_id and todo.title == title]
    
    def complete_todo(self, user_id: int, todo_id: int) -> bool:
        for todo in self.db.todos:
            if todo.user_id == user_id and todo.id == todo_id:
                todo.completed = True  # mark task as completed
                return True
        return False
    
    
