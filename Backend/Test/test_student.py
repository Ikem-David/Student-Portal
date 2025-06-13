from Backend.Test.test_Oauth2 import client
from Backend.index import app
import pytest
from Backend.db import SessionLocal
import Backend.models
import Backend.crud

db = SessionLocal()

from Backend.Routers.Oauth2 import create_access_token

admin_jwt=create_access_token(data={"sub":"ikemdavid8@gmail.com","role":"admin"})
student_jwt=create_access_token(data={"sub":"kene@example.com","role":"student"})
teacher_jwt=create_access_token(data={"sub":"john@example.com","role":"teacher"})

def test_student_get_all_courses_authorized():
    headers = {"Authorization":f"Bearer {student_jwt}"}
    factor = client.get("/student/courses/all",headers=headers)
    assert factor.status_code == 200
    assert isinstance(factor.json(),list)

def test_student_get_all_courses_not_authorized():
    headers = {"Authorization":f"Bearer {admin_jwt}"}
    factor = client.get("/student/courses/all",headers=headers)
    assert factor.status_code == 401
    assert factor.json()["detail"] == "You are not authorized to use this"

def test_student_get_all_courses_not_authorized_2():
    headers = {"Authorization":f"Bearer {teacher_jwt}"}
    factor = client.get("/student/courses/all",headers=headers)
    assert factor.status_code == 401
    assert factor.json()["detail"] == "You are not authorized to use this"

def test_get_student_courses():
    headers = {"Authorization":f"Bearer {student_jwt}"}
    response = client.get("/student/courses/my_courses",params={"matric":"22/00000"},headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not Found"

    response1 = client.get("/student/courses/my_courses",params={"matric":"22/0010"},headers=headers)
    assert response1.status_code == 200
    assert isinstance(response1.json(),list)

    headers2 = {"Authorization":f"Bearer {teacher_jwt}"}
    response2 = client.get("/student/courses/my_courses",params={"matric":"22/0010"},headers=headers2)
    assert response2.status_code == 401
    assert response2.json()["detail"] == "You are not authorized to use this"

    headers3 = {"Authorization":f"Bearer {admin_jwt}"}
    response3 = client.get("/student/courses/my_courses",params={"matric":"22/0010"},headers=headers3)
    assert response3.status_code == 401
    assert response3.json()["detail"] == "You are not authorized to use this"
 
def test_result():
    header = {"Authorization":f"Bearer {student_jwt}"}
    header2 = {"Authorization":f"Bearer {teacher_jwt}"}
    header3 = {"Authorization":f"Bearer {admin_jwt}"}

    response = client.get("/student/result",params={"matric":"22/0010"},headers=header)
    assert response.status_code == 200
    assert isinstance(response.json(),list)

    response1 = client.get("/student/result",params={"matric":"22/00000"},headers=header)
    assert response1.status_code == 404
    assert response1.json()["detail"] == "Student not Found"

    response2 = client.get("/student/result",params={"matric":"22/0010"},headers=header2)
    assert response2.status_code == 401
    assert response2.json()["detail"] == "You are not authorized to use this"

    response3 = client.get("/student/result",params={"matric":"22/0010"},headers=header3)
    assert response3.status_code == 401
    assert response3.json()["detail"] == "You are not authorized to use this"

@pytest.fixture
def test_register():
    header = {"Authorization":f"Bearer {student_jwt}"}
    header2 = {"Authorization":f"Bearer {teacher_jwt}"}
    header3 = {"Authorization":f"Bearer {admin_jwt}"}

    matric = "22/0010"
    wrong_matric = "22/00000"

    data = {"student_matric":matric,
            "level":300,
            "session":"2025/2026.1"}
    invalid = {"student_matric":wrong_matric,
                "level":300,
                "session":"2025/2026.1"}
    
    response = client.post(f"/student/{matric}/register",json=data,headers=header)
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    yield response.json()

    x = client.post(f"/student/{matric}/register",json=data,headers=header)
    assert x.status_code == 400
    assert x.json()["detail"] == "Already registered"

    db.query(Backend.models.Registration).filter(Backend.models.Registration.student_matric == matric).filter(Backend.models.Registration.session == data["session"]).delete()
    db.commit()

    response1 = client.post(f"/student/{wrong_matric}/register",json=invalid,headers=header)
    assert response1.status_code == 404
    assert response1.json()["detail"] == "Student doesn't exist"

    response2 = client.post(f"/student/{matric}/register",json=data,headers=header2)
    assert response2.status_code == 401
    assert response2.json()["detail"] == "You are not authorized to use this"

    response3 = client.post(f"/student/{matric}/register",json=data,headers=header3)
    assert response3.status_code == 401
    assert response3.json()["detail"] == "You are not authorized to use this"    

def test_add_courses():
    matric = "22/0010"
    wrong_matric = "22/00000"
    code = "cosc101"
    invalid_code = "cosc490"

    header = {"Authorization":f"Bearer {student_jwt}"}
    header2 = {"Authorization":f"Bearer {teacher_jwt}"}
    header3 = {"Authorization":f"Bearer {admin_jwt}"} 

    response = client.post(f"/student/{matric}/courses/{code}/add",headers=header)
    assert response.status_code == 200
    assert response.json() == {"Message":"Course Added"}

    response1 = client.post(f"/student/{matric}/courses/{invalid_code}/add",headers=header)
    assert response1.status_code == 404
    assert response1.json()["detail"] == "Course not found or Already Added"

    responsex = client.post(f"/student/{wrong_matric}/courses/{invalid_code}/add",headers=header)
    assert responsex.status_code == 404
    assert responsex.json()["detail"] == "Course not found or Already Added"

    Backend.crud.drop_course(db,matric,code)

    response2 = client.post(f"/student/{wrong_matric}/courses/{code}/add",headers=header2)
    assert response2.status_code == 401
    assert response2.json()["detail"] == "You are not authorized to use this"

    response3 = client.post(f"/student/{matric}/courses/{code}/add",headers=header3)
    assert response3.status_code == 401
    assert response3.json()["detail"] == "You are not authorized to use this"     


def test_drop_courses():
    matric = "22/0010"
    wrong_matric = "22/00000"
    code = "cosc101"
    invalid_code = "cosc490"

    Backend.crud.add_course_to_student(db,matric,code)

    header = {"Authorization":f"Bearer {student_jwt}"}
    header2 = {"Authorization":f"Bearer {teacher_jwt}"}
    header3 = {"Authorization":f"Bearer {admin_jwt}"} 

    response = client.delete(f"/student/{matric}/courses/my_courses/{code}/drop",headers=header)
    assert response.status_code == 200
    assert response.json() == {"Message":"Course Deleted"}

    response1 = client.delete(f"/student/{matric}/courses/my_courses/{invalid_code}/drop",headers=header)
    assert response1.status_code == 404
    assert response1.json()["detail"] == "Course or Matric not found"

    responsex = client.delete(f"/student/{wrong_matric}/courses/my_courses/{invalid_code}/drop",headers=header)
    assert responsex.status_code == 404
    assert responsex.json()["detail"] == "Course or Matric not found"

    response2 = client.delete(f"/student/{wrong_matric}/courses/my_courses/{code}/drop",headers=header2)
    assert response2.status_code == 401
    assert response2.json()["detail"] == "You are not authorized to use this"

    response3 = client.delete(f"/student/{matric}/courses/my_courses/{code}/drop",headers=header3)
    assert response3.status_code == 401
    assert response3.json()["detail"] == "You are not authorized to use this"     