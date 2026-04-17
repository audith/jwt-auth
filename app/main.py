from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from .import models,schemas,crud,auth
from.database import engine
from.dependencies import get_db,admin_only
import os

 
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.on_event("startup")
def create_admin():
    db=next(get_db())
    email=os.getenv("ADMIN_EMAIL")
    password=os.getenv("ADMIN_PASSWORD")
    if not crud.get_user_by_email(db,email):
        crud.creare_user(db,email,password,is_admin=True)


@app.post("/register")
def register(user:schemas.UserCreate,db:Session=Depends(get_db)):
    if crud.get_user_by_email(db,user.email):
        raise HTTPException(status_code=400,detail="user exist")

    return crud.creare_user(db,user.email,user.password)


@app.post("/login")
def login(data:schemas.LoginSchema,db:Session=Depends(get_db)):
    user=crud.get_user_by_email(db,data.email)
    if not user or not auth.verify_password(data.password,user.password):
        raise HTTPException(status_code=401,detail="invalid credentials")
    
    token=auth.create_token({"sub":user.email})
    return {"access_token":token}


@app.post("/admin/create_user")
def admin_create(user:schemas.UserCreate,db:Session=Depends(get_db),admine=Depends(admin_only)):
    return crud.creare_user(db,user.email,user.password)


@app.delete("/admin/delete-user/{user_id}")
def admin_delete(user_id:int,db:Session=Depends(get_db),admin=Depends(admin_only)):
    crud.delete_user(db,user_id)
    return {"massage":"userd deleted"}
    
