from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    level: int
    xp: int

    class Config:
        orm_mode = True

class LessonBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    video_url: Optional[str]
    xp_reward: int

    class Config:
        orm_mode = True
