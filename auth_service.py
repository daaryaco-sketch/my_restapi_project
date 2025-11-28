from database import JsonDatabase
from models import User
from datetime import datetime
import time

class AuthService:
    db: JsonDatabase
    sessions: dict[str, int]
    _user_counter = 0

    def __init__(self, db: JsonDatabase):
        self.db = db
        self.sessions = {}
        if len(self.db.users) == 0:
            max_id = 0
        else:
            max_id = max([user.id for user in self.db.users])
        AuthService._user_counter = max_id

    def register(self, username: str, password: str) -> User:
        if username in [user.username for user in self.db.users]:
            raise ValueError('This username already exists.')
        AuthService._user_counter += 1
        user = User(
            id=AuthService._user_counter,
            username=username,
            password_hash=password,
            created_at=datetime.today())

        self.db.users.append(user)
        self.db.save_users()
        return user

    def login(self, username: str, password: str) -> str:
        """
        :param username: name of the user
        :param password: password of the user
        :return: session token of the user
        """
        for user in self.db.users:
            if user.username == username and user.password_hash == password:
                session_token = f"{user.id}-{time.time()}"
                self.sessions[session_token] = user.id
                return session_token
        raise ValueError('Invalid username or password.')
    
    def logout(self, token: str) -> None:
        result = self.sessions.pop(token, None)
        if result is None:
            raise ValueError('Invalid token.')

    def get_user_by_token(self, token: str) -> User | None:
        user_id = self.sessions.get(token, None)
        if not user_id is None:
            for user in self.db.users:
                if user.id == user_id:
                    return user
        return None