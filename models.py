from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    created_at: datetime

@dataclass
class TodoItem:
    id: int
    user_id: int
    title: str
    completed: bool
    created_at: datetime
    