import boto3
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from requests.exceptions import SSLError
from sqlalchemy import func
from apscheduler.schedulers.background import BackgroundScheduler
from ..database import SessionLocal
from ..endpoints.potholes import create_pothole
from .. import models, crud

router = APIRouter()

scheduler = BackgroundScheduler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# .env 파일 로드
load_dotenv()

# S3 설정
iam_access_key = os.getenv("CREDENTIALS_ACCESS_KEY")
iam_secret_key = os.getenv("CREDENTIALS_SECRET_KEY")
bucket_name = os.getenv("S3_BUCKET")
api_url = os.getenv("API_URL")
region_name = "ap-northeast-2"

s3 = boto3.client('s3', aws_access_key_id=iam_access_key, aws_secret_access_key=iam_secret_key, region_name=region_name)

# 데이터베이스에 넣을 데이터 생성 함수
def create_database_entry(data):
    created_at = datetime.strptime(f"{data['trsmYear']}-{data['trsmMt']}-{data['trsmDy']} {data['trsmTm'][:2]}:{data['trsmTm'][2:4]}:{data['trsmTm'][4:]}", "%Y-%m-%d %H:%M:%S")
    return {
        "lat": str(data["vhcleLat"]),
        "lng": str(data["vhcleLot"]),
        "image": "",
        "done": -1,
        "created_at": created_at
    }

# 데이터 생성 함수
def process_data(data_sample):
    # 데이터베이스에 넣을 데이터 생성
    db_entry = create_database_entry(data_sample)
    return db_entry

# 데이터 처리 및 DB에 저장
def process_and_store_data(db: Session):
    try:
        # API로부터 JSON 데이터 가져오기
        page_no = 1
        now = datetime.now()
        thirty_minutes_ago = now - timedelta(minutes=30)
        records_processed = 0

        while records_processed < 10:
            params = {
                'pageNo': page_no,
                'numOfRows': 1000
            }
            response = requests.get(api_url, params=params, verify=False)
            response.raise_for_status()
            json_data = response.json()

            if not json_data:
                break

            # 데이터 처리 및 DB에 저장
            for data_sample in json_data:
                created_at = datetime.strptime(f"{data_sample['trsmYear']}-{data_sample['trsmMt']}-{data_sample['trsmDy']} {data_sample['trsmTm'][:2]}:{data_sample['trsmTm'][2:4]}:{data_sample['trsmTm'][4:]}", "%Y-%m-%d %H:%M:%S")
                if created_at < thirty_minutes_ago:
                    continue

                db_entry = process_data(data_sample)
                # DB에 저장하기 위해 crud 모듈의 create_pothole 호출
                pothole = models.Pothole(**db_entry)
                pothole.created_at = db_entry.get("created_at")  # 지정된 시간으로 설정
                crud.create_pothole_with_json(db=db, pothole=pothole)
                print(db_entry)

                records_processed += 1
                if records_processed >= 10:
                    break

            page_no += 1
    except SSLError as e:
        print(f"SSL Error: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

# FastAPI 엔드포인트 정의
@router.get("/process-data")
async def process_api_data(db: Session = Depends(get_db)):
    try:
        process_and_store_data(db)
        return {"message": "Data processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data processing failed: {e}")

# 30분마다 자동 실행되도록 스케줄러 설정
scheduler.add_job(lambda: next(get_db()) and process_and_store_data(next(get_db())), 'interval', minutes=30)
scheduler.start()