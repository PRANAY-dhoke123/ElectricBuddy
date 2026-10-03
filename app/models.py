from sqlalchemy import Column, Integer, Float ,String ,TIMESTAMP,ForeignKey ,CheckConstraint, UniqueConstraint ,text
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String ,nullable=False)
    email = Column(String ,nullable=False,unique = True)
    password = Column(String , nullable=False )
    role = Column(String, nullable=False, default="user")
    
    # User's electricity-board state
    state_id = Column(
        Integer,
        ForeignKey("states.id"),
        nullable=False
)

    created_at = Column(
                        TIMESTAMP(timezone=True),
                        server_default=text('now()'),
                        nullable=False
                        )


class User_data(Base):
    __tablename__ = "users_info"

    __table_args__ = ( UniqueConstraint("user_id", "month"),CheckConstraint("prev_reading >= 0"),
        CheckConstraint("curnt_reading >= prev_reading"), )

    id = Column(Integer , primary_key =True , nullable = False)
    user_id = Column(Integer  , ForeignKey("users.user_id"), nullable=False)
    month = Column(String , nullable=False)
    prev_reading = Column(Integer , nullable= False) 
    curnt_reading =Column(Integer , nullable= False) 


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True)
    state = Column(String, nullable=False, unique=True)

class State_tariff(Base):
    __tablename__ = "state_tariff"

    __table_args__ = (
        CheckConstraint("from_unit >= 0"),
        CheckConstraint("to_unit > from_unit"),
        CheckConstraint("rate_per_unit > 0"),
    )

    id = Column(Integer, primary_key=True)

    state_id = Column(
        Integer,
        ForeignKey("states.id"),
        nullable=False
    )

    from_unit = Column(Integer, nullable=False)
    to_unit = Column(Integer, nullable=False)
    rate_per_unit = Column(Float, nullable=False)

class User_tariff(Base):
    __tablename__ = "user_tariff"
    __table_args__ = (
        UniqueConstraint("user_id", "month"),
        CheckConstraint("units_consumed > 0"),
        CheckConstraint("amount > 0"),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"),nullable=False)
    month = Column(String, nullable=False)
    units_consumed = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)