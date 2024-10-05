from fastapi import FastAPI
from .database import engine
from . import models
from .endpoints import users, posts, potholes, reports
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from .service import api_scheduler

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(reports.router, prefix="/report", tags=["report"])
app.include_router(posts.router, prefix="/post", tags=["post"])
app.include_router(potholes.router, prefix="/pothole", tags=["pothole"])

#실시간 포트홀 정보 가져오는 api
app.include_router(api_scheduler.router, prefix="/api_scheduler", tags=["api_scheduler"])