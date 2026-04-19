from sqlalchemy import Column, Integer,Text,String,ForeignKey
from database import engine
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

#upload resume
class Resume(Base):
    __tablename__ = "resumes"

    id =Column(Integer,primary_key =True,index=True)
    content =Column(Text)
    skills  = Column(Text)
    experience = Column(Text)
    score = Column(Integer)
    user_id = Column(Integer,ForeignKey("users.id"))
#User authentification
class User(Base):
    __tablename__="users"

    id =Column(Integer,primary_key=True,index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

#create table
Base.metadata.create_all(bind=engine)