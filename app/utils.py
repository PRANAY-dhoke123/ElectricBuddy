# This file is for hashing the password
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password : str):
    return password_hasher.hash(password)

def verify(plain_password , hashed_password):
    return password_hasher.verify(plain_password , hashed_password)