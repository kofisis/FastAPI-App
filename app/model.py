from sqlalchemy.sql.expression import text
from sqlalchemy import Column,Integer,TIMESTAMP,String,Boolean,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship




class Users(Base):
    __table__name = "users"
    id= Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    location=Column(String,nullable=False)
    published=Column(Boolean,nullable=False,server_default="True")
    ratings=Column(Integer,nullable=False,server_default="0")
    created_at=Column(TIMESTAMP,nullable=False,server_default=text("NOW()"))
    owner_id= Column(Integer,ForeignKey("registration.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("Registration")

class Registration(Base):
    __table__name = "registration"
    id=Column(Integer, nullable=False,primary_key=True)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))