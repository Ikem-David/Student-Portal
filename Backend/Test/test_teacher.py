from Backend.Routers.Oauth2 import create_access_token

admin_jwt=create_access_token(data={"sub":"ikemdavid8@gmail.com","role":"admin"})
student_jwt=create_access_token(data={"sub":"kene@example.com","role":"student"})
teacher_jwt=create_access_token(data={"sub":"john@example.com","role":"teacher"})

from fastapi.testclient import TestClient
from Backend.index import app
from Backend.Test.test_Oauth2 import client
import Backend.models
from sqlalchemy.orm import Session as db
import pytest

def test_get_all_courses():
    headers = {"Authorization":f"Bearer {teacher_jwt}"}
    factor = client.get("/teacher/courses",headers=headers)
    assert factor.status_code == 200
    assert isinstance(factor.json(),list)

    sheaders = {"Authorization":f"Bearer {student_jwt}"}
    sfactor = client.get("/teacher/courses",headers=sheaders)
    assert sfactor.status_code == 401
    assert sfactor.json()["detail"] == "You are not authorized to use this"

    headersa = {"Authorization":f"Bearer {admin_jwt}"}
    afactor = client.get("/teacher/courses",headers=headersa)
    assert afactor.status_code == 401
    assert afactor.json()["detail"] == "You are not authorized to use this"

@pytest.fixture
def test_upload_result():
    student_headers = {"Authorization":f"Bearer {student_jwt}"}
    test = client.post("/teacher/upload/result",headers=student_headers,json=data)
    assert test.status_code == 401 
    assert test.json()["detail"] == "You are not authorized to use this"

    admin_headers = {"Authorization":f"Bearer {admin_jwt}"}
    test = client.post("/teacher/upload/result",headers=admin_headers,json=data)
    assert test.status_code == 401
    assert test.json()["detail"] == "You are not authorized to use this"


    data = {"student_matric":"22/0010","course_code":"cosc101","score":80}
    headers = {"Authorization":f"Bearer {teacher_jwt}"}
    response = client.post("/teacher/upload/result",headers=headers,json=data)
    assert response.status_code == 200
    assert isinstance(response.json(),dict)

    already_data = {"student_matric":"22/0010","course_code":"cosc101","score":80}
    already_headers = {"Authorization":f"Bearer {teacher_jwt}"}
    already_response = client.post("/teacher/upload/result",headers=already_headers,json=already_data)
    assert already_response.status_code == 400
    assert already_response.json()['detail'] == "Result already exists"

    yield response.json()
    db.query(Backend.models.Results).filter(Backend.models.Results.id == response.json()["id"]).delete()
    db.commit()

    invalid_data = {"student_matric":"22/0010","course_code":"cosc1058","score":80}
    headersa = {"Authorization":f"Bearer {teacher_jwt}"}
    invalid_response = client.post("/teacher/upload/result",headers=headersa,json=invalid_data)
    assert invalid_response.status_code == 400
    assert invalid_response.json()["detail"] == "Course doesn't exist"