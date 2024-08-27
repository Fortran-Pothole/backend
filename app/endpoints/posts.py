from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
def read_posts_done(post_id: int, db: Session = Depends(get_db)):
    posts = crud.get_post(db, post_id)
    return posts




@router.get("/done/{done}", response_model=list[schemas.Post])
def read_posts_done(done: int, db: Session = Depends(get_db)):
    posts = crud.get_posts_done(db, done)
    return posts

@router.patch("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.update_post(db=db, post_id=post_id, post=post)


@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db=db, post_id=post_id)

@router.post("/pothole")
def create_pothole_with_post(pothole: schemas.PotholeCreate, post: schemas.PostCreatePothole, db: Session = Depends(get_db)):
    # Pothole 객체 생성
    db_pothole = crud.create_pothole(db=db, pothole=pothole)
    db_post = crud.create_post_with_pothole(db=db, post=schemas.PostCreate(
        user_id=post.user_id,
        content=post.content,
        done=post.done
    ), pothole_id=db_pothole.id)
    
    return {"pothole": db_pothole, "post": db_post}