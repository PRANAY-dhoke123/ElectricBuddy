from pydantic import BaseModel,EmailStr , ConfigDict
from datetime import datetime



class UserCreate(BaseModel):
    
    name : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str


class UserOut(BaseModel):
    id : int
    email : EmailStr
    model_config = ConfigDict(from_attributes=True)
