from fastapi import APIRouter

router = APIRouter()

@router.get('/register')
def test():
  return {"Hey": "Dude"}

@router.post('/register')
def register():

  return