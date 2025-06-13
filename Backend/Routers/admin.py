from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.db import get_db
import Backend.crud
from Backend.models import UserRole
import Backend.schema
import Backend.models
from .Oauth2 import oauth2_schema, current_user, required_role
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])


# Get All
@router.get("/manage_users/students/all", response_model=List[Backend.schema.StudentBase])
def get_all_students(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_students(db)


@router.get("/manage_users/teachers/all", response_model=List[Backend.schema.TeacherBase])
def get_all_teachers(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_teachers(db)


@router.get("/manage_users/admin/all", response_model=List[Backend.schema.AdminBase])
def get_all_admins(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_admin(db)


@router.get("/courses/all", response_model=List[Backend.schema.CourseBase])
def get_all_courses(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_courses(db)


@router.get("/results/all", response_model=List[Backend.schema.ResultBase])
def get_all_results(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_results(db)


@router.get("/student/registered/all", response_model=List[Backend.schema.RegistrationBase])
def get_all_registered_students(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_registration_records(db)


# Get
@router.get("/manage_users/students/{matric:path}", response_model=Backend.schema.StudentBase)
def get_student(
    matric: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    student = Backend.crud.get_student(db, matric)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/manage_users/teachers/{staff_no:path}", response_model=Backend.schema.TeacherBase)
def get_teacher(
    staff_no: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    teacher = Backend.crud.get_teacher(db, staff_no)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.get("/manage_users/admins/{staff_no:path}", response_model=Backend.schema.AdminBase)
def get_admin(
    staff_no: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    admin = Backend.crud.get_admin(db, staff_no)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


@router.get("/result/{matric:path}/{code:path}", response_model=Backend.schema.ResultBase)
def get_result(
    matric: str,
    code: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    result = Backend.crud.get_result(db, matric, code)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@router.get("/course/{code:path}", response_model=Backend.schema.CourseBase)
def get_course(
    code: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    course = Backend.crud.get_course(db, code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/registered_students/", response_model=Backend.schema.Registration)
def get_registered_student(
    matric: str,
    session: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    register = Backend.crud.get_registered_student(db, matric, session)
    if not register:
        raise HTTPException(status_code=404, detail="Student not found")
    return register


# Create
@router.post("/manage_users/student/create", response_model=Backend.schema.StudentBase)
def create_student(
    guide: Backend.schema.CreateStudent,
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    student = Backend.crud.get_student(db, guide.matric_no)
    verify1 = Backend.crud.verify_student_number(db, guide.number)
    verify2 = Backend.crud.verify_teacher_number(db, guide.number)
    verify3 = Backend.crud.verify_admin_number(db, guide.number)
    verify4 = Backend.crud.verify_admin_staff_no(db, guide.matric_no)
    verify5 = Backend.crud.verify_teacher_staff_no(db, guide.matric_no)
    verify6 = Backend.crud.verify_matric(db, guide.matric_no)
    verify_auth = Backend.crud.get_auth_user(guide.email, db)

    if student:
        raise HTTPException(status_code=400, detail="Student already exists")
    if verify1:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify2:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify3:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify4:
        raise HTTPException(status_code=400, detail="Matric already exists")
    if verify5:
        raise HTTPException(status_code=400, detail="Matric already exists")
    if verify6:
        raise HTTPException(status_code=400, detail="Matric already exists")
    if verify_auth:
        raise HTTPException(status_code=400, detail="Email already exists")

    auth_data = Backend.schema.AuthUser(
        email=guide.email, password=guide.password, role=UserRole.student
    )
    Backend.crud.create_auth_user(user=auth_data, db=db)
    return Backend.crud.create_student(db, guide)


@router.post("/manage_users/teacher/create", response_model=Backend.schema.TeacherBase)
def create_teacher(
    guide: Backend.schema.CreateTeacher,
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    teacher = Backend.crud.get_teacher(db, guide.email)
    verify1 = Backend.crud.verify_teacher_number(db, guide.number)
    verify2 = Backend.crud.verify_admin_number(db, guide.number)
    verify3 = Backend.crud.verify_student_number(db, guide.number)
    verify4 = Backend.crud.verify_admin_staff_no(db, guide.staff_no)
    verify5 = Backend.crud.verify_teacher_staff_no(db, guide.staff_no)
    verify6 = Backend.crud.verify_matric(db, guide.staff_no)
    verify_auth = Backend.crud.get_auth_user(guide.email, db)

    if teacher:
        raise HTTPException(status_code=400, detail="Teacher already exists")
    if verify1:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify2:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify3:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify4:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify5:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify6:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify_auth:
        raise HTTPException(status_code=400, detail="Email already exists")

    auth_data = Backend.schema.AuthUser(
        email=guide.email, password=guide.password, role=UserRole.teacher
    )
    Backend.crud.create_auth_user(user=auth_data, db=db)
    return Backend.crud.create_teacher(db, guide)


@router.post("/manage_users/admin/create", response_model=Backend.schema.AdminBase)
def create_admin(
    guide: Backend.schema.CreateAdmin,
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    admin = Backend.crud.get_admin(db, guide.email)
    verify1 = Backend.crud.verify_admin_number(db, guide.number)
    verify2 = Backend.crud.verify_student_number(db, guide.number)
    verify3 = Backend.crud.verify_teacher_number(db, guide.number)
    verify4 = Backend.crud.verify_admin_staff_no(db, guide.staff_no)
    verify5 = Backend.crud.verify_teacher_staff_no(db, guide.staff_no)
    verify6 = Backend.crud.verify_matric(db, guide.staff_no)
    verify_auth = Backend.crud.get_auth_user(guide.email, db)

    if admin:
        raise HTTPException(status_code=400, detail="Admin already exists")
    if verify1:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify2:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify3:
        raise HTTPException(status_code=400, detail="Number already exists")
    if verify4:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify5:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify6:
        raise HTTPException(status_code=400, detail="Staff_no already exists")
    if verify_auth:
        raise HTTPException(status_code=400, detail="Email already exists")
    else:
        auth_data = Backend.schema.AuthUser(
            email=guide.email, password=guide.password, role=UserRole.admin
        )
        Backend.crud.create_auth_user(user=auth_data, db=db)
        return Backend.crud.create_admin(db, guide)


@router.post("/courses/create", response_model=Backend.schema.CourseBase)
def create_course(
    guide: Backend.schema.CreateCourse,
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    course = Backend.crud.get_course(db, guide.code)
    verify = Backend.crud.verify_course(db, guide.name)
    if course:
        raise HTTPException(status_code=400, detail="Course already exists")
    if verify:
        raise HTTPException(status_code=400, detail="Course name already exists")
    else:
        return Backend.crud.create_course(db, guide)


# Update
@router.put("/manage_users/student/update/", response_model=Backend.schema.StudentBase)
def update_student(
    matric: str,
    student: Backend.schema.UpdateStudent,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_student(db, matric)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not Found")
    else:
        return Backend.crud.update_student(db, matric, student)


@router.put("/manage_users/teacher/update/", response_model=Backend.schema.TeacherBase)
def update_teacher(
    staff_no: str,
    teacher: Backend.schema.UpdateTeacher,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_teacher(db, staff_no)
    if not existing:
        raise HTTPException(status_code=404, detail="Teacher not Found")
    else:
        return Backend.crud.update_teacher(db, staff_no, teacher)


@router.put("/manage_users/admin/update/", response_model=Backend.schema.AdminBase)
def update_admin(
    staff_no: str,
    admin: Backend.schema.UpdateAdmin,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    admin = Backend.crud.get_admin(db, staff_no)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not Found")
    else:
        return Backend.crud.update_admin(db, staff_no, admin)


@router.put("/course/update/", response_model=Backend.schema.CourseBase)
def update_course(
    code: str,
    course: Backend.schema.UpdateCourse,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_course(db, code)
    if not existing:
        raise HTTPException(status_code=404, detail="Course not Found")
    else:
        return Backend.crud.update_course(db, code, course)


# Delete
@router.delete("/manage_users/student/delete/{matric:path}/{email:path}")
def delete_student(
    matric: str,
    email: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    student = Backend.crud.get_student(db, matric)
    if not student:
        raise HTTPException(status_code=404, detail="Student not Found")
    else:
        Backend.crud.delete_auth_user(email, db)
        Backend.crud.delete_student(db, matric)
        return {"Message": "Student Deleted"}


@router.delete("/manage_users/teacher/delete/{staff_no:path}")
def delete_teacher(
    staff_no: str,
    email: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    teacher = Backend.crud.get_teacher(db, staff_no)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not Found")
    else:
        Backend.crud.delete_auth_user(email, db)
        Backend.crud.delete_teacher(db, staff_no)
        return {"Message": "Teacher Deleted"}


@router.delete("/manage_users/admin/delete/{staff_no:path}")
def delete_admin(
    staff_no: str,
    email: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    admin = Backend.crud.get_admin(db, staff_no)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not Found")
    else:
        Backend.crud.delete_auth_user(email, db)
        Backend.crud.delete_admin(db, staff_no)
        return {"Message": "Admin Deleted"}


@router.delete("/course/delete/{code:path}")
def delete_course(
    code: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["admin"])),
    db: Session = Depends(get_db),
):
    course = Backend.crud.get_course(db, code)
    if not course:
        raise HTTPException(status_code=404, detail="Course not Found")
    else:
        Backend.crud.delete_course(db, code)
        return {"Message": "Course Deleted"}
