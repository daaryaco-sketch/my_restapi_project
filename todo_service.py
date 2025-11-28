from database import JsonDatabase
from models import TodoItem
from datetime import datetime

class TodoService:
    db: JsonDatabase
    _todo_counter = 0

    def __init__(self, db: JsonDatabase):
        self.db = db
        max_todo = len(self.db.todos)
        if  max_todo == 0:
            TodoService._todo_counter = 0
        else:
            TodoService._todo_counter = max([todo.id for todo in self.db.todos])

    def create_todo(self, user_id: int, title: str) -> TodoItem:
        if user_id not in [user.id for user in self.db.users]:
            raise Exception(f"User {user_id} does not exist")
        self._todo_counter += 1
        todo = TodoItem(
            id=self._todo_counter,
            user_id=user_id,
            title=title,
            completed=False,
            created_at=datetime.today())
        self.db.todos.append(todo)
        self.db.save_todos()
        return todo
    
    def list_todos(self, user_id: int) -> list[TodoItem]:
        return [todo for todo in self.db.todos if todo.user_id == user_id]
    
    def complete_todo(self, user_id: int, todo_id: int) -> bool:
        for todo in self.db.todos:
            if todo.user_id == user_id and todo.id == todo_id:
                todo.completed = True  # mark task as completed
                self.db.save_todos()
                return True
        return False
    
    def delete_todo(self, user_id: int, todo_id: int) -> bool:
        for todo in self.db.todos:
            if todo.user_id == user_id and todo.id == todo_id:
                self.db.todos.remove(todo)
                self.db.save_todos()
                return True
        return False