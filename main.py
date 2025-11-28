from database import JsonDatabase
from auth_service import AuthService
from todo_service import TodoService
from api import ApiSimulator

if __name__ == "__main__":

    db = JsonDatabase("users.json", "todos.json")

    try:
        db.load_users()
        db.load_todos()
    except FileNotFoundError as e:
        print(e)
    try:
        authSrv = AuthService(db)
        todoSrv = TodoService(db)
        api = ApiSimulator(authSrv, todoSrv)

        user = api.post_register('reza02', '12345')
        token = list(api.post_login('reza02', '12345').values())[0]

        api.post_todo_create(token, "Programing")
        api.post_todo_create(token, "Designing")
        api.post_todo_create(token, "Creating")

        list_dict_todos = api.get_todos(token)
        for list_todo in list_dict_todos:
            print({key:value for key,value in list_todo.items()})

        api.post_todo_complete(token, 1)
        api.post_todo_delete(token, 1)

        list_dict_todos = api.get_todos(token)
        for list_todo in list_dict_todos:
            print({key: value for key, value in list_todo.items()})

        print(api.post_logout(token))

    except Exception as ex:
        print(ex)


