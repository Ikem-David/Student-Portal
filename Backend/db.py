from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# URL = "mysql+pymysql://fastapi_user:your_password@localhost/vehicle_tracking"

# CREATE DATABASE (DB NAME);
# CREATE USER 'USERNAME_user'@'localhost' IDENTIFIED BY 'your_password';
# GRANT ALL PRIVILEGES ON DB NAME.* TO 'USERNAME_user'@'localhost';
# FLUSH PRIVILEGES;

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

