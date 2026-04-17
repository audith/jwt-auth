from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:str
    is_admin:bool

    class Config:
        orm_mode=True


class LoginSchema(BaseModel):
    email:EmailStr
    password:str