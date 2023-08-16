import pytest
from app import schemas
from .database import client, session
from jose import jwt
from app.config import settings



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))

#     # assert res.json().get('message') == "Hello World"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json={"email":"hello1234@gmail.com","password":"password123"})

    
    new_user = schemas.User(**res.json())
    assert new_user.email == "hello1234@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})

    login = schemas.Token(**res.json())

    payload = jwt.decode(login.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")

    # assert res.json().get("email") == "hello1234@gmail.com"
    assert res.status_code == 200
    assert id == test_user["id"]
    assert login.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com','password123',403),
    ('sanjeev@gmail.com','wrongpass',403),
    (None,'password123',422),
    ('sanjeev@gmail.com',None,422)
])
def test_incorrect_login(test_user,client,email, password, status_code):
    res = client.post("/login",data={"username":email,
                                     "password":password})
    

    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"