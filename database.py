from pathlib import Path
from models import User, TodoItem
from datetime import datetime
import json

class JsonDatabase:
    users_file: Path
    todos_file: Path
    users: list[User]
    todos: list[TodoItem]

    def __init__(self, users_file: Path, todos_file: Path):
        self.users_file = users_file
        self.todos_file = todos_file

    def load_users(self) -> None:
        if not Path.exists(self.users_file):
            raise ValueError('Path does not exists.')
        with open(self.users_file, 'r') as file:
            json_users = json.load(file)
            self.users = [User(
                id = int(value['id']),
                username = value['username'],
                password_hash = value['password_hash'],
                created_at = datetime.fromisoformat(value['created_at'])
            ) for key, value in json_users.items()]

    def save_users(self) -> None:
        if not Path.exists(self.users_file):
            raise ValueError('Path does not exists.')
        dict_users = {user.id:{
                            'id': user.id,
                            'username': user.username,
                            'password_hash': user.password_hash,
                            'created_at': str(user.created_at)
            }for user in self.users}
        with open(self.users_file, "w") as file:
            json.dump(dict_users, file, indent=4)
