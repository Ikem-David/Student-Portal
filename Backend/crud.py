from sqlalchemy.orm import Session
import Backend.models
from Backend.models import UserRole
import Backend.schema
from passlib.context import CryptContext

Encoder = CryptContext(schemes=['bcrypt'], deprecated="auto")

class Hash:
    @staticmethod
    def hasher(password: str) -> str:
        return Encoder.hash(password)

    @staticmethod
    def verifier(hashed: str, plaintext: str) -> bool:
        return Encoder.verify(plaintext, hashed)

# Get single entity
def get_student(db:Session,matric:str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    if student:
        return student
    else:
        return None

def verify_student_number(db:Session,number:str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.number == number).first()
    if student:
        return student
    else:
        return None

def verify_student_email(db:Session,email:str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.email == email).first()
    if student:
        return student
    else:
        return None
    
def get_student_courses(db:Session,matric:str):  
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    if student:
        return student.courses
    else:
        return None

def get_student_results(db:Session,matric:str):  
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    if student:
        return student.result
    else:
        return None

def get_teacher(db:Session,staff_no:str):
    teacher = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.staff_no == staff_no).first()
    if teacher:
        return teacher
    else:
        return None
    
def verify_teacher_number(db:Session,number:str):
    teacher = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.number == number).first()
    if teacher:
        return teacher
    else:
        return None

def verify_teacher_email(db:Session,email:str):
    teacher = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.email == email).first()
    if teacher:
        return teacher
    else:
        return None
    
def get_result(db:Session,matric:str,code:str):
    result = db.query(Backend.models.Results).filter(Backend.models.Results.student_matric == matric).filter(Backend.models.Results.course_code == code).first()
    if result:
        return result
    else:
        return None

def get_course(db:Session,code:str):
    course = db.query(Backend.models.Courses).filter(Backend.models.Courses.code == code).first()
    if course:
        return course
    else:
        return None

def verify_course(db:Session,name:str):
    course = db.query(Backend.models.Courses).filter(Backend.models.Courses.name == name).first()
    if course:
        return course
    else:
        return None

def get_admin(db:Session,staff_no:str):
    admin = db.query(Backend.models.Admin).filter(Backend.models.Admin.staff_no == staff_no).first()
    if admin:
        return admin
    else:
        return None
    
def verify_admin_number(db:Session,number:str):
    admin = db.query(Backend.models.Admin).filter(Backend.models.Admin.number == number).first()
    if admin:
        return admin
    else:
        return None

def verify_admin_email(db:Session,email:str):
    admin = db.query(Backend.models.Admin).filter(Backend.models.Admin.email == email).first()
    if admin:
        return admin
    else:
        return None

def get_registered_student(db:Session,matric:str,session:str):
    registered = db.query(Backend.models.Registration).filter(Backend.models.Registration.student_matric == matric).filter(Backend.models.Registration.session == session).first()
    if registered:
        return registered
    else:
        return None
    
# Get all entities
def get_all_students(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Students).offset(skip).limit(limit).all()

def get_all_teachers(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Teacher).offset(skip).limit(limit).all()

def get_all_admin(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Admin).offset(skip).limit(limit).all()

def get_all_results(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Results).offset(skip).limit(limit).all()

def get_all_courses(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Courses).offset(skip).limit(limit).all()

def get_all_registration_records(db:Session,skip:int=0,limit:int=100):
    return db.query(Backend.models.Registration).offset(skip).limit(limit).all()

# Delete
def delete_student(db: Session, matric: str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

def delete_teacher(db: Session, staff_no: str):
    teacher = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.staff_no == staff_no).first()
    if teacher:
        db.delete(teacher)
        db.commit()
        return True
    return False

def delete_result(db: Session, matric: str, code: str):
    result = db.query(Backend.models.Results).filter(
        Backend.models.Results.student_matric == matric,
        Backend.models.Results.course_code == code
    ).first()
    if result:
        db.delete(result)
        db.commit()
        return True
    return False

def delete_course(db: Session, code: str):
    course = db.query(Backend.models.Courses).filter(Backend.models.Courses.code == code).first()
    if course:
        db.delete(course)
        db.commit()
        return True
    return False

def delete_admin(db: Session, staff_no: str):
    admin = db.query(Backend.models.Admin).filter(Backend.models.Admin.staff_no == staff_no).first()
    if admin:
        db.delete(admin)
        db.commit()
        return True
    return False

def delete_registered_student(db: Session, matric: str,session:str):
    registered = db.query(Backend.models.Registration).filter(Backend.models.Registration.student_matric == matric).filter(Backend.models.Registration.session == session).first()
    if registered:
        db.delete(registered)
        db.commit()
        return True
    return False

# Create
def create_student(db:Session,student:Backend.schema.CreateStudent):
    data = Backend.models.Students(
        name = student.name,
        matric_no = student.matric_no,
        age = student.age,
        number =student.number,
        level =student.level,
        email =student.email,
        role = UserRole.student,
        password = Hash.hasher(student.password),
        department =student.department
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def add_course_to_student(db: Session, matric_no: str, course_code: str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric_no).first()
    course = db.query(Backend.models.Courses).filter(Backend.models.Courses.code == course_code).first()
    if not student or not course:
        return None
    
    if course in student.courses:
        return None
    
    else:
        student.courses.append(course)
        db.commit()
        db.refresh(student)
        return student

def drop_course(db:Session,matric_no:str,course_code:str):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric_no).first()
    course = db.query(Backend.models.Courses).filter(Backend.models.Courses.code == course_code).first()

    if not student or not course:
        return None
    
    if course in student.courses:
        student.courses.remove(course)
        db.commit()
        db.refresh(student)
        return student 
    
    else:
        return None


def create_teacher(db:Session,teacher:Backend.schema.CreateTeacher):
    data = Backend.models.Teacher(
        name = teacher.name,
        staff_no = teacher.staff_no,
        age = teacher.age,
        number = teacher.number,
        email = teacher.email,
        role = UserRole.teacher,
        password = Hash.hasher(teacher.password),
        department = teacher.department
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def create_admin(db:Session,admin:Backend.schema.CreateAdmin):
    data = Backend.models.Admin(
        name = admin.name,
        staff_no = admin.staff_no,
        age = admin.age,
        number = admin.number,
        email = admin.email,
        role = UserRole.admin,
        password = Hash.hasher(admin.password),        
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def create_course(db:Session,course:Backend.schema.CreateCourse):
    data = Backend.models.Courses(
        name = course.name,
        code = course.code,
        department = course.department
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def create_result(db:Session,result:Backend.schema.CreateResult):
    data = Backend.models.Results(
        student_matric = result.student_matric,
        course_code = result.course_code,
        score = result.score
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def append_result(matric:str,code:str,db:Session):
    student = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    resul = db.query(Backend.models.Results).filter(Backend.models.Results.student_matric == matric).filter(Backend.models.Results.course_code == code).first()

    if not student or not resul:
        return None
    
    student.result.append(resul)
    db.commit()
    db.refresh(student)
    return student

def create_registered(db:Session,register:Backend.schema.CreateRegistration,courses:list[str]):
    data = Backend.models.Registration(
        student_matric = register.student_matric,
        level = register.level,
        session = register.session,
        courses = courses
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# Update
def update_student(db: Session, matric: str, student: Backend.schema.UpdateStudent):
    data = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric).first()
    
    if not data:
        return None

    if student.name is not None:
        data.name = student.name
    if student.age is not None:
        data.age = student.age
    if student.email is not None:
        data.email = student.email
    if student.matric_no is not None:
        data.matric_no = student.matric_no
    if student.department is not None:
        data.department = student.department
    if student.level is not None:
        data.level = student.level
    if student.number is not None:
        data.number = student.number
    if student.password is not None:
        data.password = Hash.hasher(student.password)

    db.commit()
    db.refresh(data)
    return data


def update_teacher(db: Session, staff_no: str, teacher: Backend.schema.UpdateTeacher):
    data = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.staff_no == staff_no).first()
    
    if not data:
        return None

    if teacher.name is not None:
        data.name = teacher.name
    if teacher.staff_no is not None:
        data.staff_no = teacher.staff_no
    if teacher.age is not None:
        data.age = teacher.age
    if teacher.number is not None:
        data.number = teacher.number
    if teacher.email is not None:
        data.email = teacher.email
    if teacher.password is not None:
        data.password = Hash.hasher(teacher.password)
    if teacher.department is not None:
        data.department = teacher.department

    db.commit()
    db.refresh(data)
    return data

def update_admin(db: Session, staff_no: str, admin: Backend.schema.UpdateAdmin):
    data = db.query(Backend.models.Admin).filter(Backend.models.Admin.staff_no == staff_no).first()
    
    if not data:
        return None

    if admin.name is not None:
        data.name = admin.name
    if admin.staff_no is not None:
        data.staff_no = admin.staff_no        
    if admin.age is not None:
        data.age = admin.age
    if admin.number is not None:
        data.number = admin.number
    if admin.email is not None:
        data.email = admin.email
    if admin.password is not None:
        data.password = Hash.hasher(admin.password)

    db.commit()
    db.refresh(data)
    return data

def update_course(db: Session, code: str, course: Backend.schema.UpdateCourse):
    data = db.query(Backend.models.Courses).filter(Backend.models.Courses.code == code).first()
    
    if not data:
        return None

    if course.name is not None:
        data.name = course.name
    if course.code is not None:
        data.code = course.code
    if course.department is not None:
        data.department = course.department

    db.commit()
    db.refresh(data)
    return data

def update_result(db: Session, result_id: int, result: Backend.schema.UpdateResult):
    data = db.query(Backend.models.Results).filter(Backend.models.Results.id == result_id).first()
    
    if not data:
        return None

    if result.student_matric is not None:
        data.student_matric = result.student_matric
    if result.course_code is not None:
        data.course_code = result.course_code
    if result.score is not None:
        data.score = result.score

    db.commit()
    db.refresh(data)
    return data

def update_registration(db: Session, reg_id: int, registration: Backend.schema.UpdateRegistration):
    data = db.query(Backend.models.Registration).filter(Backend.models.Registration.id == reg_id).first()
    
    if not data:
        return None

    if registration.student_matric is not None:
        data.student_matric = registration.student_matric
    if registration.level is not None:
        data.level = registration.level
    if registration.session is not None:
        data.session = registration.session

    db.commit()
    db.refresh(data)
    return data

def create_auth_user(user:Backend.schema.AuthUser,db:Session):
    data = Backend.models.AuthUsers(
        email = user.email,
        password = Hash.hasher(user.password),
        role = user.role
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

def delete_auth_user(email:str,db:Session):
    data = db.query(Backend.models.AuthUsers).filter(Backend.models.AuthUsers.email == email).first()
    if not data:
        return None
    db.delete(data)
    db.commit()

def get_auth_user(email:str,db:Session):
    data =  db.query(Backend.models.AuthUsers).filter(Backend.models.AuthUsers.email == email).first()
    if data:
        return data
    else:
        return None

# ##
def verify_matric(db:Session,matric_no:str):
    data = db.query(Backend.models.Students).filter(Backend.models.Students.matric_no == matric_no).first()
    if data:
        return data
    else:
        return None
    
def verify_teacher_staff_no(db:Session,staff_no:str):
    teacher = db.query(Backend.models.Teacher).filter(Backend.models.Teacher.staff_no == staff_no).first()
    if teacher:
        return teacher
    else:
        return None

def verify_admin_staff_no(db:Session,staff_no:str):
    teacher = db.query(Backend.models.Admin).filter(Backend.models.Admin.staff_no == staff_no).first()
    if teacher:
        return teacher
    else:
        return None
    
