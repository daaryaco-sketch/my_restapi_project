import auth_service
from auth_service import AuthService
from todo_service import TodoService
from models import User

class ApiSimulator:
    auth_service: AuthService
    todo_service: TodoService
    
    def __init__(self):
        pass

    '''
    def require_auth(func):
        def wrapper(self, token = None, *args, **kwargs):
            user = self.auth_service.get_user_by_token(token)
            func(self, user, *args, **kwargs)
        return wrapper
    '''

    def post_register(self, username: str, password: str) -> dict:
        user = self.auth_service.register(username, password)
        return {user.id:{
            'id': user.id,
            'username': user.username,
            'password': user.password_hash,
            'created_at': user.created_at,
        }}

    def post_login(self, username: str, password: str) -> dict:
        session_token = self.auth_service.login(username, password)
        return {username:session_token}

    def post_logout(self, token: str) -> dict:
        user = self.auth_service.get_user_by_token(token)
        if user is None:
            return {"error": "Unauthorized"}
        self.auth_service.logout(token)
        return {"success": False}

    def post_todo_create(self, token: str, title: str) -> dict:
        user = self.auth_service.get_user_by_token(token)
        if user is None:
            return {"error": "Unauthorized"}
        todo = self.todo_service.create_todo(user.id, title)
        self.todo_service.db.save_todos()
        return {todo.id:{
            'id': todo.id,
            'user_id': todo.user_id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at,
        }}

    def get_todos(self, token: str) -> list[dict]:
        user = self.auth_service.get_user_by_token(token)
        if user is None:
            return [{"error": "Unauthorized"}]
        todos = self.todo_service.list_todos(user.id)
        return [{todo.id:{
            'id': todo.id,
            'user_id': todo.user_id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at
        } for todo in todos}]

    def post_todo_complete(self, token: str, todo_id: int) -> dict:
        user = self.auth_service.get_user_by_token(token)
        if user is None:
            return {"error": "Unauthorized"}
        self.todo_service.complete_todo(user.id, todo_id)
        self.todo_service.db.save_todos()
        return {"success": True}

    def post_todo_delete(self, token: str, todo_id: int) -> dict:
        user = self.auth_service.get_user_by_token(token)
        if user is None:
            return {"error": "Unauthorized"}
        self.todo_service.delete_todo(user.id, todo_id)
        self.todo_service.db.save_todos()
        return {"success": True}