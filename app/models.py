from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import random
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # id는 자동 생성
    name = Column(String(50), index=True)
    password = Column(String(20), nullable=False)
    phone = Column(String(12), nullable=False)  # 전화번호 필드 추가
    reports = relationship("Report", back_populates="owner")

class Pothole(Base):
    __tablename__ = "potholes"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(Text, index=True)
    lat = Column(String(255), index=True)
    lng = Column(String(255), index=True)
    done = Column(Integer, default=-1)
                    # 처리 전 -1
                    # 처리 중 0
                    # 처리 완료 1
    report_count = Column(Integer, default=0)  # 동일한 위치의 Report 수를 저장하는 필드
    warning = Column(Integer, default=lambda: random.randint(1, 5))  # 1~5 사이의 랜덤 정수
    created_at = Column(DateTime(timezone=True))
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
    content = Column(Text, index=True)
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
    location = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    done = Column(Integer, default=-1)
                    # 처리 전 -1
                    # 처리 중 0
                    # 처리 완료 1
    images = Column(Text, default="https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/V3F_HY_1562_20160212_013414_N_CH2_Seoul_Sun_Highway_Day_84497.png")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="reports")
    # notice_count = 
