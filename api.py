from auth_service import AuthService
from todo_service import TodoService

class ApiSimulator:
    auth_service: AuthService
    todo_service: TodoService
    
    def __init__(self):
        pass

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
        return {"success":False}
