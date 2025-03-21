from sqlalchemy.orm import Session
from . import models, schemas
from faker import Faker
from fastapi import HTTPException
from datetime import datetime

fake = Faker()

images_list = [
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/V3F_HY_1562_20160212_013414_N_CH2_Seoul_Sun_Highway_Day_84497.png",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/502d1f78-da20-48c9-b1b4-9729021391a1.jpg",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/2c39bb91-c9ae-4143-b62f-7fd22003ab31.jpg",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/0977579c-8ac4-46d6-9178-d75276d7bfbf.jpg",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/8bcba1a1-ba02-4e78-9cef-141a0d123033.jpg"
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/8bcba1a1-ba02-4e78-9cef-141a0d123033.jpg",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/a8a743d4-7bc1-4755-8c9e-59e5c3e93f78.jpg",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/p2.png",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/p1.png",
    "https://fortran-pothole.s3.ap-northeast-2.amazonaws.com/p3.jpg"
]

image_index = 0

def get_next_image():
    global image_index
    # 현재 인덱스에 해당하는 이미지 선택
    image = images_list[image_index]
    image_index = (image_index + 1) % len(images_list)
    return image

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, password=user.password, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def get_all_users(db: Session):
    return db.query(models.User).all()

def is_name_taken(db: Session, name: str) -> bool:
    return db.query(models.User).filter(models.User.name == name).first() is not None

# Pothole CRUD functions
def get_pothole(db: Session, pothole_id: int):
    return db.query(models.Pothole).filter(models.Pothole.id == pothole_id).first()

def get_potholes(db: Session):
    return db.query(models.Pothole).all()

def get_potholes_done(db: Session, done: int = 0):
    return db.query(models.Pothole).filter(models.Pothole.done == done)

def create_pothole(db: Session, pothole: schemas.PotholeCreate):
    created_at = datetime.now()
    if pothole.warning:
        db_pothole = models.Pothole(lat=pothole.lat, lng=pothole.lng, done=pothole.done, image=pothole.image, created_at=created_at, warning=pothole.warning)
    else:
        db_pothole = models.Pothole(lat=pothole.lat, lng=pothole.lng, done=pothole.done, image=pothole.image, created_at=created_at)
    db.add(db_pothole)
    db.commit()
    db.refresh(db_pothole)
    return db_pothole


def create_pothole_with_json(db: Session, pothole: schemas.PotholeCreateJson):
    db_pothole = models.Pothole(lat=pothole.lat, lng=pothole.lng, done=pothole.done, image=pothole.image, created_at=pothole.created_at)
    db.add(db_pothole)
    db.commit()
    db.refresh(db_pothole)
    return db_pothole

def update_pothole(db: Session, pothole_id: int, pothole: schemas.PotholeUpdate):
    db_pothole = db.query(models.Pothole).filter(models.Pothole.id == pothole_id).first()
    if db_pothole:
        db_pothole.done = pothole.done
        db.commit()
        db.refresh(db_pothole)
    return db_pothole


def delete_pothole(db: Session, pothole_id: int):
    db_pothole = db.query(models.Pothole).filter(models.Pothole.id == pothole_id).first()
    if db_pothole:
        db.delete(db_pothole)
        db.commit()
    return db_pothole


# Post CRUD functions
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session):
    return db.query(models.Post).all()

def get_posts_done(db: Session, done: int):
    return db.query(models.Post).filter(models.Post.done == done)

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(pothole_id=post.pothole_id, user_id=post.user_id, content=post.content, done=post.done)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_post_with_pothole(db: Session, post: schemas.PostCreate, pothole_id: int):
    db_post = models.Post(
        pothole_id=pothole_id,  # 여기서 전달된 pothole_id 사용
        user_id=post.user_id,
        content=post.content,
        done=post.done
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        if post.content is not None:
            db_post.content = post.content
        if post.done is not None:
            db_post.done = post.done
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post

def create_report(db: Session, report: schemas.ReportCreateImg):
    db_report = models.Report(
        location=report.location,
        content=report.content,
        user_id=report.user_id, # 사용자의 ID를 외래 키로 설정
        images=get_next_image()
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def create_report_img(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(
        location=report.location,
        content=report.content,
        user_id=report.user_id,
        images=report.images  # S3에서 받은 이미지 URL을 저장
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_reports(db: Session):
    return db.query(models.Report).all()

def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if report:
        db.delete(report)
        db.commit()
    return report

def update_report_done(db: Session, report_id: int, done: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.done = done  # done 상태 업데이트
    db.commit()
    db.refresh(report)
    return report

def delete_all_potholes(db: Session):
    db.query(models.Pothole).delete()
    db.commit()
