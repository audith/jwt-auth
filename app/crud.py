from sqlalchemy.orm import Session
from .models import User
from .auth import hash_password


def create_user(db: Session, password: str, email: str, is_admin: bool = False):
    user = User(
        email=email,
        password=hash_password(password),
        is_admin=is_admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return user