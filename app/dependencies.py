from fastapi import Depends,HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
import os

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str,db:Session=Depends(get_db)):
    try:
        playload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user=db.query(User).filter(User.email == playload["sub"]).first()
    except:
        raise HTTPException(status_code=401,detail="invalid user name")
    



