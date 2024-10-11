from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import boto3
import os
from datetime import datetime
from typing import List
from .. import crud, schemas
from ..database import SessionLocal
from jmunja import smssend
# import json


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.Report)
def create_report(report: schemas.ReportCreateImg, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

# AWS S3 설정
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# S3 클라이언트 생성
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

@router.post("/img", response_model=schemas.ReportCreate)
async def create_report_with_image(
    location: str = Form(...),  # Form으로 본문 데이터 받기
    content: str = Form(...),  # Form으로 본문 데이터 받기
    user_id: int = Form(...),  # Form으로 본문 데이터 받기    
    images: UploadFile = File(...),  # 이미지 파일을 받는 부분
    db: Session = Depends(get_db)
):
    try:
        # 문자열로 받은 JSON 데이터를 파싱
        # report_data = json.loads(report)
        # report_obj = schemas.ReportCreateImg(**report_data)

        # 파일 이름 생성 (유니크하게 만들기 위해 날짜와 원본 파일명을 조합)
        image_filename = f"{datetime.now().isoformat()}_{images.filename}"
        
        # S3에 이미지 업로드
        s3_client.upload_fileobj(images.file, 
                                AWS_BUCKET_NAME, 
                                image_filename,
                                ExtraArgs={'ContentType': images.content_type}  # Content-Type 지정
)
        
        # S3 URL 생성
        image_url = f"https://{AWS_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image_filename}"
        
        # Report 생성할 때 image URL을 포함
        new_report = schemas.ReportCreate(
            location=location,
            content=content,
            images=image_url,
            user_id=user_id
        )
        
        return crud.create_report_img(db=db, report=new_report)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

