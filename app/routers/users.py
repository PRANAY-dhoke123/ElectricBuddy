#This file is for all the request for the user 

from .. import models , schemas , utils
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(  prefix="/users",tags=["Users"])

#this will create a new  user entry in table 
@router.post("/", response_model = schemas.UserOut  )
def create_user(user : schemas.UserCreate , db: Session = Depends(get_db)):
    
    #Hash the password :
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user