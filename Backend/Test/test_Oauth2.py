from fastapi.testclient import TestClient
from Backend.index import app

client = TestClient(app)

def test_login():
    login = client.post("/token",data={"username":"ikemdavid8@gmail.com",
                                       "password":"Firstpoint0"})
    assert login.status_code == 200
    assert "access_token" in login.json()
    assert login.json()["token_type"] == "bearer"

def test_login_wrong_username():
    login = client.post("/token",data={"username":"wrong@gmail.com",
                                       "password":"Firstpoint0"})
    assert login.status_code == 404
    assert login.json()["detail"] == "Wrong Username"

def test_login_wrong_password():
    login = client.post("/token",data={"username":"ikemdavid8@gmail.com",
                                       "password":"wrong"})
    assert login.status_code == 404
    assert login.json()["detail"] == "Wrong Password"