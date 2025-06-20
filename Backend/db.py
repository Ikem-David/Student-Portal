from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

db_url = "mysql+pymysql://fastapi_user:your_password@localhost/student"

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

