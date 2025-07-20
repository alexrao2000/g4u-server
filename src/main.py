from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.database import Base, engine
from src.routes.auth import router as auth_router

import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
  Base.metadata.create_all(bind=engine)
  yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:5173'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(auth_router, prefix='/auth')

@app.get('/')
def read_root():
  return {"Hello": "World"}

@app.get('/referral-code')
def get_referral_code():
  referral_code = uuid.uuid4().hex[:8] # 名字， 字母， 六位alphanumeric
  return {"code": referral_code}

  #一个人不能超过99推荐