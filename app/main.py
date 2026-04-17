from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine
from .dependencies import get_db, admin_only
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# -------------------------
# CREATE ADMIN ON STARTUP
# -------------------------
@app.on_event("startup")
def create_admin():
    db = next(get_db())

    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not crud.get_user_by_email(db, email):
        crud.create_user(
            db=db,
            email=email,
            password=password,
            is_admin=True
        )


# -------------------------
# REGISTER USER
# -------------------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    return crud.create_user(
        db=db,
        email=user.email,
        password=user.password
    )


# -------------------------
# LOGIN
# -------------------------
@app.post("/login")
def login(data: schemas.LoginSchema, db: Session = Depends(get_db)):

    user = crud.get_user_by_email(db, data.email)

    if not user or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token({"sub": user.email})

    return {"access_token": token}


# -------------------------
# ADMIN CREATE USER
# -------------------------
@app.post("/admin/create_user")
def admin_create(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    return crud.create_user(
        db=db,
        email=user.email,
        password=user.password,
        is_admin=True
    )


# -------------------------
# ADMIN DELETE USER
# -------------------------
@app.delete("/admin/delete-user/{user_id}")
def admin_delete(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    deleted = crud.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}