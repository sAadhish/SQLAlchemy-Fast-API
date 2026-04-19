from pydantic import BaseModel,Field

class Resume(BaseModel):
    content : str = Field(min_length=20)

class UserCreate(BaseModel):
    username : str =Field(min_length=3)
    password : str 

