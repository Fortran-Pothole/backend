from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    phone: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Pothole schemas
class PotholeBase(BaseModel):
    lat: str
    lng: str
    image: str
    done: int = -1 #swagger에 있는 default 값

class PotholeCreate(PotholeBase):
    pass

class PotholeCreateJson(PotholeBase):
    created_at: datetime

class PotholeUpdate(BaseModel):
    done: int

class Pothole(PotholeBase):
    id: int
    image: str
    warning: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    user_id: int
    content: str
    done: int = -1  # swagger에 있는 default 값

class PostCreatePothole(PostBase):
    pass

class PostCreate(PostBase):
    pothole_id: int

class PostUpdate(BaseModel):
    content: Optional[str] = None
    done: Optional[int] = None

class Post(PostBase):
    id: int
    pothole_id: int

    class Config:
        orm_mode = True

class ReportBase(BaseModel):
    location: str
    content: str
    images: str  # 이미지 파일 이름 리스트
    user_id: int  # 작성자 ID를 포함

class ReportCreate(ReportBase):
    pass

class ReportCreateImg(BaseModel):
    location: str
    content: str
    user_id: int  # 작성자 ID를 포함

class Report(ReportBase):
    id: int
    created_at: datetime
    user_id: int  # 작성자 ID 포함
    done: int


    class Config:
        orm_mode = True
    
class ReportUpdate(BaseModel):
    done: int

class SMSRequest(BaseModel):
    hpno: str  # 핸드폰 번호를 받아오기 위한 필드