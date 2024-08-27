from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import random
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # id는 자동 생성
    name = Column(String, index=True)
    password = Column(String, nullable=False)
    reports = relationship("Report", back_populates="owner")

class Pothole(Base):
    __tablename__ = "potholes"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, index=True)
    lat = Column(String, index=True)
    lng = Column(String, index=True)
    done = Column(Integer, default=-1)
                    # 처리 전 -1
                    # 처리 중 0
                    # 처리 완료 1
    report_count = Column(Integer, default=0)  # 동일한 위치의 Report 수를 저장하는 필드
    warning = Column(Integer, default=lambda: random.randint(1, 5))  # 1~5 사이의 랜덤 정수
    posts = relationship("Post", cascade="all, delete-orphan", back_populates="pothole")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'warning' not in kwargs:
            self.warning = random.randint(1, 5)  # 1~5 사이의 랜덤 정수로 초기화

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    pothole_id = Column(Integer, ForeignKey("potholes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, index=True)
    done = Column(Integer, default=-1)
                    # 처리 전 -1
                    # 처리 중 0
                    # 처리 완료 1
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")
    pothole = relationship("Pothole", back_populates="posts")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pothole_id = Column(Integer, ForeignKey("potholes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    images = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="reports")
    # notice_count = 
