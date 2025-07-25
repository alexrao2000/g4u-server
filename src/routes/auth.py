from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import ArgumentError, IntegrityError

from src.models.user import User
from src.database import get_db

import uuid
import bcrypt

router = APIRouter()

class UserModel(BaseModel):
  email: str
  password: str

@router.post('/register')
def register(data: UserModel, db: Session=Depends(get_db)):

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
  
  except IntegrityError:

    db.rollback()
    exception = HTTPException(status_code=400, detail="Email already has an account associated with it.")
    #print(exception)

    raise exception
  
  except:

    exception = HTTPException(status_code=400, detail="Error: Something went wrong.")

    raise exception
  
@router.post('/login')
def login(data: UserModel, db: Session=Depends(get_db)):
  try:
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
      raise HTTPException(status_code=404, detail="User not found.")
    
    if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
      raise HTTPException(status_code=401, detail="Wrong password.")
    
    accessToken = str(uuid.uuid4())
    
    return JSONResponse({"message": "Success!", "accessToken": accessToken})
  except ArgumentError:
    raise HTTPException(status_code=500, detail="ArgumentError: Invalid or conflicting function argument")
  
  except:
    raise HTTPException(status_code=400, detail="You messed up something else, not sure what it is.")
