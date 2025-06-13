from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime,timedelta,UTC
from jose import jwt,JWTError
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Backend.db import get_db
import Backend.models
import Backend.crud
from Backend.schema import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "gTSYwRJ5zIWIPjg8vU7sgvdioah8pPXoqyHBD59OoAwMnsyUPZ8xXQ=="
ALGORITHM = "HS256"
ACCESS_KEY_EXPIRE_MINUTES = 30

def create_access_token(data:dict,expire_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(UTC) + expire_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_KEY_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise credentials    
    except JWTError:
        raise credentials

    user = Backend.crud.get_auth_user(username,db)

    if user is None:
        raise credentials
    return user

router = APIRouter(tags=["Authentication"])

@router.post("/token")
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(Backend.models.AuthUsers).filter(Backend.models.AuthUsers.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wrong Username")
    if not Backend.crud.Hash.verifier(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Wrong Password")
    else:
        access_token = create_access_token(data={'sub':user.email,'role':user.role})
        return {
            "access_token":access_token,
            "token_type":"bearer",
            "email":user.email,
            "role":user.role
        }
    
def required_role(required_role:list[str]):
    def role_checker(user:User=Depends(current_user)):
        if user.role not in required_role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to use this")
        return user
    return role_checker