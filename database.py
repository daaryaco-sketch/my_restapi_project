from pathlib import Path
from models import User, TodoItem
from datetime import datetime
import json

class JsonDatabase:
    users_file: Path
    todos_file: Path
    users: list[User]
    todos: list[TodoItem]

    def __init__(self, users_file, todos_file):
        self.users_file = users_file
        self.todos_file = todos_file
        self.users = []
        self.todos = []

    def load_users(self) -> None:
        usr_file = Path(self.users_file)
        if usr_file.exists():
            raise FileNotFoundError('File does not exists.')
        with open(self.users_file, 'r') as file:
            json_users = json.load(file)
            self.users = [User(
                id = int(value['id']),
                username = value['username'],
                password_hash = value['password_hash'],
                created_at = datetime.fromisoformat(value['created_at'])
            ) for key, value in json_users.items()]

    def save_users(self) -> None:
        dict_users = {user.id:{
                            'id': user.id,
                            'username': user.username,
                            'password_hash': user.password_hash,
                            'created_at': str(user.created_at)
            }for user in self.users}
        with open(self.users_file, "w") as file:
            json.dump(dict_users, file, indent=4)

    def load_todos(self) -> None:
        todo_file = Path(self.todos_file)
        if todo_file.exists():
            raise FileNotFoundError('Path does not exists')
        with open(self.todos_file, 'r') as file:
            dict_todos = json.load(file)
            self.todos = [TodoItem(
                                    id = int(value['id']),
                                    user_id = int(value['user_id']),
                                    title = value['title'],
                                    completed = bool(value['completed']),
                                    created_at = datetime.fromisoformat(value['created_at'])
            ) for key, value in dict_todos.items()]
    
    def save_todos(self) -> None:
        dict_todos = {todo.id:{
                'id': todo.id,
                'user_id': todo.user_id,
                'title': todo.title,
                'completed': todo.completed,
                'created_at': str(todo.created_at)
        }for todo in self.todos}
        with open(self.todos_file, 'w') as file:
            json.dump(dict_todos, file, indent=4)
    
