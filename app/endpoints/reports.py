from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal
from jmunja import smssend


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

@router.get("/{report_id}", response_model=schemas.Report)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.get("", response_model=List[schemas.Report])
def read_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db=db)

@router.delete("/{report_id}", response_model=schemas.Report)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.delete_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

uid = "portrancapstone"
upw = "34eb0a89dcbf268691b116c2b11704"
subject = "[Fortran] 포트홀 신고 관련 안내"
content = "수동 등록하신 포트홀이 처리 완료되었습니다. 앱을 통해 확인해주세요."
@router.put("/{report_id}", response_model=schemas.Report)
def update_report(report_id: int, report: schemas.ReportUpdate, sms_request: schemas.SMSRequest, db: Session = Depends(get_db)):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    jphone = smssend.JmunjaPhone(uid, upw)
    jphone.send(subject, content, sms_request.hpno)
    jweb = smssend.JmunjaWeb(uid, upw)
    jweb.send(subject, content, sms_request.hpno, sms_request.hpno)

    return crud.update_report_done(db=db, report_id=report_id, done=report.done)

