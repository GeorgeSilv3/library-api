import pytest, requests

BASE_URL = "http://127.0.0.1:5000"
id_test = 0

def test_add_book():
    global id_test
    data = {
        "name": "TestBook",
        "author": "George",
        "edition": "2nd"
        }
    response = requests.post(f"{BASE_URL}/books", json=data)
    id_test = response.json()["id"]
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200


def test_get_book():
    response = requests.get(f"{BASE_URL}/books/{id_test}")
    print(id_test)
    assert response.status_code == 200
    assert response.json()["id"] == id_test

