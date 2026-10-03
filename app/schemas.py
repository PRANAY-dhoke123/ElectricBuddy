from pydantic import BaseModel,EmailStr , ConfigDict
from datetime import datetime


# user register schema
class UserCreate(BaseModel):    
    name : str
    email : EmailStr
    password : str
    state: str
# after registration user response schema
class UserOut(BaseModel):
    name : str
    email : EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email : EmailStr
    password : str
