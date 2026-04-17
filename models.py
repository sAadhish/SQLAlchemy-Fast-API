from sqlalchemy import Column, Integer,Text
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id =Column(Integer,primary_key =True,index=True)
    content =Column(Text)
    skills  = Column(Text)
    experience = Column(Text)
    score = Column(Integer)
    

#create table
Base.metadata.create_all(bind=engine)