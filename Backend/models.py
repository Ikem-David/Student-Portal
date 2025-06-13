from sqlalchemy import String, Integer, Column, Table, ForeignKey,JSON,Enum as SqlEnum
from sqlalchemy.orm import relationship
from Backend.db import Base
from enum import Enum

Student_Course = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)

Student_Registration = Table(
    "students_registration",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("register_id", Integer, ForeignKey("registration.id")),
)

Student_Result = Table(
    "student_result",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("result_id", Integer, ForeignKey("results.id")),
)

Teacher_Course = Table(
    "teacher_courses",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)

class UserRole(str,Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class DepartmentEnum(str, Enum):
    computer_science = "Computer Science"
    electrical_engineering = "Electrical Engineering"
    mechanical_engineering = "Mechanical Engineering"
    civil_engineering = "Civil Engineering"
    mathematics = "Mathematics"
    physics = "Physics"
    chemistry = "Chemistry"
    biology = "Biology"
    business_admin = "Business Administration"
    accounting = "Accounting"
    economics = "Economics"
    english = "English"
    history = "History"


class AuthUsers(Base):
    __tablename__ = "authusers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(SqlEnum(UserRole),nullable=False)

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    matric_no = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    number = Column(String(100), nullable=False, unique=True)
    level = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(SqlEnum(UserRole.student),nullable=False,server_default=UserRole.student.value)
    password = Column(String(100), nullable=False)
    department = Column(SqlEnum(DepartmentEnum), nullable=False)

    courses = relationship("Courses", secondary=Student_Course, back_populates="students")
    result = relationship("Results", secondary=Student_Result, back_populates="student")
    register = relationship(
        "Registration", secondary=Student_Registration, back_populates="student"
    )


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    staff_no = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    number = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(SqlEnum(UserRole),nullable=False,server_default=UserRole.teacher.value)
    department = Column(SqlEnum(DepartmentEnum), nullable=False)

    course = relationship("Courses", secondary=Teacher_Course, back_populates="teacher")


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    staff_no = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    number = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(SqlEnum(UserRole),nullable=False,server_default=UserRole.admin.value)
    password = Column(String(100), nullable=False)


class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(100), nullable=False, unique=True)
    department = Column(SqlEnum(DepartmentEnum), nullable=False)

    students = relationship("Students", secondary=Student_Course, back_populates="courses")
    teacher = relationship("Teacher", secondary=Teacher_Course, back_populates="course")


class Results(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_matric = Column(String(100), nullable=False)
    course_code = Column(String(100), nullable=False)
    score = Column(Integer, nullable=False)

    student = relationship("Students", secondary=Student_Result, back_populates="result")


class Registration(Base):
    __tablename__ = "registration"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_matric = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    session = Column(String(100), nullable=False)
    courses = Column(JSON,nullable=False)

    student = relationship(
        "Students", secondary=Student_Registration, back_populates="register"
    )