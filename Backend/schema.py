from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal
from Backend.models import UserRole, DepartmentEnum


# Student
class StudentBase(BaseModel):
    name: str
    matric_no: str
    age: int
    number: str
    level: int
    email: EmailStr
    department: DepartmentEnum


class CreateStudent(StudentBase):
    password: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    matric_no: Optional[str] = None
    age: Optional[int] = None
    number: Optional[str] = None
    level: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    department: Optional[DepartmentEnum] = None


class Student(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


# Teacher
class TeacherBase(BaseModel):
    name: str
    staff_no: str
    age: int
    number: str
    email: EmailStr
    department: DepartmentEnum


class CreateTeacher(TeacherBase):
    password: str


class UpdateTeacher(BaseModel):
    name: Optional[str] = None
    staff_no: Optional[str] = None
    age: Optional[int] = None
    number: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    department: Optional[DepartmentEnum] = None


class Teacher(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


# Admin
class AdminBase(BaseModel):
    name: str
    staff_no: str
    age: int
    number: str
    email: EmailStr


class CreateAdmin(AdminBase):
    password: str


class UpdateAdmin(BaseModel):
    name: Optional[str] = None
    staff_no: Optional[str] = None
    age: Optional[int] = None
    number: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Admin(AdminBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


# Course
class CourseBase(BaseModel):
    name: str
    code: str
    department: DepartmentEnum


class CreateCourse(CourseBase):
    pass


class UpdateCourse(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    department: Optional[DepartmentEnum] = None


class Course(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


# Result
class ResultBase(BaseModel):
    student_matric: str
    course_code: str
    score: int


class CreateResult(ResultBase):
    pass


class UpdateResult(BaseModel):
    student_matric: Optional[str] = None
    course_code: Optional[str] = None
    score: Optional[int] = None


class Result(ResultBase):
    id: int
    model_config = ConfigDict(from_attributes = True)


# Registration
class RegistrationBase(BaseModel):
    student_matric: str
    level: int
    session: str
    courses:list[str]
    model_config = ConfigDict(from_attributes = True)


class CreateRegistration(BaseModel):
    student_matric: str
    level: int
    session: str

class UpdateRegistration(BaseModel):
    student_matric: Optional[str] = None
    level: Optional[int] = None
    session: Optional[str] = None


class Registration(RegistrationBase):
    id: int
    model_config = ConfigDict(from_attributes = True)

# Auth Users
class AuthUser(BaseModel):
    email:EmailStr
    password:str
    role:UserRole

class User(BaseModel):
    email:EmailStr 
    role:UserRole