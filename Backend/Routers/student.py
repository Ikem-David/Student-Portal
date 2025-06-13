from fastapi import APIRouter, Depends, HTTPException
from Backend.db import get_db
import Backend.schema
import Backend.crud
from sqlalchemy.orm import Session
from .Oauth2 import current_user, required_role
from typing import List
import Backend.models

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/courses/all", response_model=List[Backend.schema.CourseBase])
def get_courses(
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_courses(db)


@router.get("/courses/my_courses", response_model=List[Backend.schema.CourseBase])
def get_my_courses(
    matric: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_student(db, matric)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not Found")
    return Backend.crud.get_student_courses(db, matric)


@router.get("/result", response_model=List[Backend.schema.ResultBase])
def get_my_results(
    matric: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_student(db, matric)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not Found")
    return Backend.crud.get_student_results(db, matric)


@router.post("/{matric:path}/register", response_model=Backend.schema.Registration)
def register(
    matric: str,
    register: Backend.schema.CreateRegistration,
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    existing = Backend.crud.get_student(db, register.student_matric)
    add_courses = Backend.crud.get_student_courses(db, register.student_matric)
    already = Backend.crud.get_registered_student(db, register.student_matric, register.session)
    if add_courses is None or len(add_courses) == 0:
        raise HTTPException(status_code=401, detail="Add courses before registering")
    if not existing:
        raise HTTPException(status_code=400, detail="Student doesn't exist")
    if already:
        raise HTTPException(status_code=400, detail="Already registered")
    register_course = [course.code for course in add_courses]
    return Backend.crud.create_registered(db, register, courses=register_course)


@router.post("/{matric:path}/courses/{code:path}/add")
def add_courses(
    matric: str,
    code: str,
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    exist = Backend.crud.add_course_to_student(db, matric, code)
    if exist is None:
        raise HTTPException(status_code=404, detail="Course not found or Already Added")
    else:
        return {"Message": "Course Added"}


@router.delete("/{matric:path}/courses/my_courses/{code:path}/drop")
def drop_course(
    matric: str,
    code: str,
    current_user: Backend.schema.User = Depends(current_user),
    user=Depends(required_role(["student"])),
    db: Session = Depends(get_db),
):
    exist = Backend.crud.drop_course(db, matric, code)
    if exist is None:
        raise HTTPException(status_code=404, detail="Course or Matric not found")
    return {"Message": "Course Deleted"}
