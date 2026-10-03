#This file is for all the request for the user 

from .. import models , schemas , utils
from fastapi import Depends, APIRouter , HTTPException
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(  prefix="/users",tags=["Users"])

#this will create a new  user entry in table 
@router.post("/", response_model = schemas.UserOut  )
def create_user(user : schemas.UserCreate , db: Session = Depends(get_db)):
    
    #Hash the password :
    hashed_password = utils.hash_password(user.password)
    # adding state 
    state = db.query(models.State).filter(models.State.state == user.state ).first()
    if not state :
        raise HTTPException(status_code = 404 , detail = "State Not Found")
    new_user = models.User(user_id = utils.generate_user_id(db),
                            name=user.name,
                            email=user.email,
                            password=hashed_password,
                            state_id=state.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user