from pydantic import BaseModel
from typing import Optional

# User schemas
class UserBase(BaseModel):
    pass  # No name field here, as it will be generated randomly

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    name: str  # Name field here to display it in responses

    class Config:
        orm_mode = True

# Pothole schemas
class PotholeBase(BaseModel):
    lat: str
    lng: str
    done: int = -1 #swagger에 있는 default 값

class PotholeCreate(PotholeBase):
    pass


class PotholeUpdate(BaseModel):
    done: int

class Pothole(PotholeBase):
    id: int

    class Config:
        orm_mode = True

# Post schemas
class PostBase(BaseModel):
    pothole_id: int
    user_id: int
    content: str
    done: int = -1 #swagger에 있는 default 값

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None
    done: Optional[int] = None

class Post(PostBase):
    id: int

    class Config:
        orm_mode = True
