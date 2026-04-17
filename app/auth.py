from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# -------------------------
# ARGON2 CONFIG (NEW)
# -------------------------
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# -------------------------
# PASSWORD FUNCTIONS
# -------------------------

def hash_password(password: str):
    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    password = password.strip()

    # No 72-byte limit anymore (argon2 is safe for long passwords)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    if not plain_password or not hashed_password:
        return False

    return pwd_context.verify(plain_password, hashed_password)


# -------------------------
# JWT TOKEN
# -------------------------

def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)