from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal

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
