import pytest, requests

BASE_URL = "http://127.0.0.1:5000"

def test_add_book():
    data = {
        "name": "TestBook",
        "author": "George",
        "edition": "2nd"
        }
    response = requests.post(f"{BASE_URL}/books", json=data)

    assert response.status_code == 200
    assert "message" in response.json()

def test_get_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200