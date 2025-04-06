# fastapi-app/tests/test_external_api.py

import requests

def test_external_get():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert "userId" in response.json()
