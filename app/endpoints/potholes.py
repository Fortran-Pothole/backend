from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from jmunja import smssend


uid = "portrancapstone"
upw = "34eb0a89dcbf268691b116c2b11704"
subject = "[Fortran] 포트홀 신고 관련 안내"
content = "등록하신 포트홀이 처리 완료되었습니다. 앱을 통해 확인해주세요."

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

@router.post("/with_json", response_model=schemas.Pothole)
def create_pothole_with_json(pothole: schemas.PotholeCreateJson, db: Session = Depends(get_db)):
    return crud.create_pothole_with_json(db=db, pothole=pothole)

@router.get("/", response_model=list[schemas.Pothole])
def read_potholes(db: Session = Depends(get_db)):
    potholes = crud.get_potholes(db)
    return potholes

@router.get("/{pothole_id}", response_model=schemas.Pothole)
def read_potholes(pothole_id: int, db: Session = Depends(get_db)):
    potholes = crud.get_pothole(db, pothole_id)
    return potholes

@router.get("/done/{done}", response_model=list[schemas.Pothole])
def read_potholes_done(done: int, db: Session = Depends(get_db)):
    potholes = crud.get_potholes_done(db, done)
    return potholes

@router.put("/{pothole_id}", response_model=schemas.Pothole)
def update_pothole(pothole_id: int, pothole: schemas.PotholeUpdate, sms_request: schemas.SMSRequest, db: Session = Depends(get_db)):
    db_pothole = crud.get_pothole(db, pothole_id=pothole_id)
    if db_pothole is None:
        raise HTTPException(status_code=404, detail="Pothole not found")
    jphone = smssend.JmunjaPhone(uid, upw)
    jphone.send(subject, content, sms_request.hpno)
    jweb = smssend.JmunjaWeb(uid, upw)
    jweb.send(subject, content, sms_request.hpno, sms_request.hpno)

    return crud.update_pothole(db=db, pothole_id=pothole_id, pothole=pothole)

@router.delete("/{pothole_id}", response_model=schemas.Pothole)
def delete_pothole(pothole_id: int, db: Session = Depends(get_db)):
    db_pothole = crud.get_pothole(db, pothole_id=pothole_id)
    if db_pothole is None:
        raise HTTPException(status_code=404, detail="Pothole not found")
    return crud.delete_pothole(db=db, pothole_id=pothole_id)