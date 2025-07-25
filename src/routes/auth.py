from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.user import User
from src.database import get_db

import uuid
import bcrypt

router = APIRouter()

class UserModel(BaseModel):
  email: str
  password: str

@router.post('/register')
async def register(data: UserModel, db: Session=Depends(get_db)):

  try:
    id = str(uuid.uuid4())

    pw_bytes = data.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pw_bytes, salt)
    hashed_password = hashed_bytes.decode('utf-8')

    user = User(uuid=id, email=data.email, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    #print("ID:", id, "Email:", data.email, "Password:", hashed_password)

    response = JSONResponse(status_code=200, content={"message": "Success!"})

    return response
  
  except:

    exception = HTTPException(status_code=400, detail="Email already has an account associated with it.")
    #print(exception)

    raise exception