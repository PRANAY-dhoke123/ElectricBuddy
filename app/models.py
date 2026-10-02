from sqlalchemy import Column, Integer, Float ,String ,TIMESTAMP ,text
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String ,nullable=False)
    email = Column(String ,nullable=False,unique = True)
    password = Column(String , nullable=False )
    role = Column(String, nullable=False, default="user")
    created_at = Column(
                        TIMESTAMP(timezone=True),
                        server_default=text('now()'),
                        nullable=False
                        )


class User_data(Base):
    __tablename__ = "users_info"

    id = Column(Integer , primary_key =True , nullable = False)
    user_id = Column(Integer  , nullable=False)
    month = Column(String , nullable=False)
    prev_reading = Column(Integer , nullable= False) 
    curnt_reading =Column(Integer , nullable= False) 


class State(Base):
    __tablename__ = "state_data"

    id = Column(Integer, primary_key=True, nullable=False)
    state = Column(String , nullable = False )
    from_unit = Column(Integer , nullable=False)
    to_unit = Column(Integer , nullable=False)
    rate_per_unit = Column(Float, nullable=False)

class User_tariff(Base):
    __tablename__ = "user_tariff"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    units_consumed = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)