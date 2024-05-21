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

@router.post("/", response_model=schemas.Pothole)
def create_pothole(pothole: schemas.PotholeCreate, db: Session = Depends(get_db)):
    return crud.create_pothole(db=db, pothole=pothole)

@router.get("/", response_model=list[schemas.Pothole])
def read_potholes(db: Session = Depends(get_db)):
    potholes = crud.get_potholes(db)
    return potholes


@router.get("/done", response_model=list[schemas.Pothole])
def read_potholes_done(done: int = 0, db: Session = Depends(get_db)):
    potholes = crud.get_potholes_done(db, done)
    return potholes

@router.put("/{pothole_id}", response_model=schemas.Pothole)
def update_pothole(pothole_id: int, pothole: schemas.PotholeUpdate, db: Session = Depends(get_db)):
    db_pothole = crud.get_pothole(db, pothole_id=pothole_id)
    if db_pothole is None:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return crud.update_pothole(db=db, pothole_id=pothole_id, pothole=pothole)


@router.delete("/{pothole_id}", response_model=schemas.Pothole)
def delete_pothole(pothole_id: int, db: Session = Depends(get_db)):
    db_pothole = crud.get_pothole(db, pothole_id=pothole_id)
    if db_pothole is None:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return crud.delete_pothole(db=db, pothole_id=pothole_id)