from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:5173'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

@app.get('/')
def read_root():
  return {"Hello": "World"}

@app.get('/referral-code')
def get_referral_code():
  referral_code = uuid.uuid4().hex[:8]
  return {"code": referral_code}