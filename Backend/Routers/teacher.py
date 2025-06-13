from fastapi import APIRouter, Depends, HTTPException
from Backend.db import get_db
import Backend.schema
import Backend.crud
from .Oauth2 import current_user, required_role
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.get("/courses", response_model=List[Backend.schema.CourseBase])
def get_all_courses(
    current_user: Backend.schema.User = Depends(current_user),
    user: Backend.schema.User = Depends(required_role(["teacher"])),
    db: Session = Depends(get_db),
):
    return Backend.crud.get_all_courses(db)


@router.post("/upload/result", response_model=Backend.schema.ResultBase)
def create_result(
    result: Backend.schema.ResultBase,
    user: Backend.schema.User = Depends(required_role(["teacher"])),
    db: Session = Depends(get_db),
):
    result_existing = Backend.crud.get_result(db, result.student_matric, result.course_code)

    course_existing = Backend.crud.get_course(db, result.course_code)

    if not course_existing:
        raise HTTPException(status_code=400, detail="Course doesn't exist")
    if result_existing:
        raise HTTPException(status_code=400, detail="Result already exists")
    else:
        new_result = Backend.crud.create_result(db, result)
        Backend.crud.append_result(result.student_matric, result.course_code, db)
        return new_result
