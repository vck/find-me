import requests

BASE_URL = "http://127.0.0.1:5000"


def test_get_todos():
    response = requests.get(f"{BASE_URL}/items")
    print(response.json())
    return response


def test_create_todo():
    todo_data = {"text": "Test todo", "status": False}
    response = requests.post(f"{BASE_URL}/items", json=todo_data)
    print(response.json())
    return response


def test_update_todo_text(todo_id, new_text):
    data = {"text": new_text}
    response = requests.put(f"{BASE_URL}/items/{todo_id}", json=data)
    print(response.json())
    return response



def test_update_todo_status(todo_id, new_status):
    data = {"status": new_status}
    response = requests.put(f"{BASE_URL}/items/{todo_id}/status", json=data)
    print(response.json())
    return response



if __name__ == "__main__":
    # Run the tests
    all_todos = test_get_todos()
    new_todos = test_create_todo()

    # Assume you have a todo with id=1 to update
    test_update_todo_text(new_todos.json()["id"], "Updated text")
    test_update_todo_status(new_todos.json()["id"], True)
