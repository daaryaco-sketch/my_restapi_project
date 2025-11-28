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
            completed=false,
            created_at=datetime.today())
        