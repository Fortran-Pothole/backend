from fastapi import FastAPI
from .database import engine
from . import models
from .endpoints import users, posts, potholes
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(potholes.router, prefix="/potholes", tags=["potholes"])