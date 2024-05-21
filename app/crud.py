from sqlalchemy.orm import Session
from . import models, schemas
from faker import Faker

fake = Faker()

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    random_name = fake.name()  # Generate a random name using Faker
    db_user = models.User(name=random_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Add similar CRUD operations for Pothole and Post

# Pothole CRUD functions
def get_pothole(db: Session, pothole_id: int):
    return db.query(models.Pothole).filter(models.Pothole.id == pothole_id).first()

def get_potholes(db: Session):
    return db.query(models.Pothole).all()

def get_potholes_done(db: Session, done: int = 0):
    return db.query(models.Pothole).filter(models.Pothole.done == done)

def create_pothole(db: Session, pothole: schemas.PotholeCreate):
    db_pothole = models.Pothole(lat=pothole.lat, lng=pothole.lng, done=pothole.done)
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

def get_posts_done(db: Session, done: int = 0):
    return db.query(models.Pothole).filter(models.Pothole.done == done)

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(pothole_id=post.pothole_id, user_id=post.user_id, content=post.content, done=post.done)
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