# This file is for hashing the password , creating a 6 digit random user_id 
from pwdlib import PasswordHash
from . import models
import random 


password_hasher = PasswordHash.recommended()

def hash_password(password : str):
    return password_hasher.hash(password)

def verify(plain_password , hashed_password):
    return password_hasher.verify(plain_password , hashed_password)


def generate_user_id(db):
    while True:
        user_id = random.randint(100000 , 999999)

        existing_id  = db.query(models.User).filter(models.User.user_id == user_id ).first()

        if not existing_id:
            return user_id