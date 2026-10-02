from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text
from .routers import users
app = FastAPI()


# @app.get('/')
# async def root():
#     print("MY First Fastapi Testing ")
#     return "Welcome to My ELECTRICBUDDY website "

# @app.get("/")
# def test(db: Session = Depends(get_db)):
#     return {"message": "API working"}

     
@app.get("/")
def test_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    print("Database Connection Sucessfull : ")
    return {
        "message": "Database connected successfully!"
    }


app.include_router(users.router)