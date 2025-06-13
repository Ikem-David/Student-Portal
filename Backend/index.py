from fastapi import FastAPI
from Backend.Routers import admin, student, teacher, Oauth2
from Backend.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(Oauth2.router)


@app.get("/")
def index():
    return {"Message": "Student Portal"}
