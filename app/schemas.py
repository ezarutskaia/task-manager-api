from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
