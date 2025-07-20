from fastapi import APIRouter
from src.models.user import User

router = APIRouter()

@router.post('/register')
def register(username, password):

  print(username, password)

  return {"message": "Success!"}