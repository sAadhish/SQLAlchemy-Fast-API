from pydantic import BaseModel,Field

class Resume(BaseModel):
    content : str = Field(min_length=10)
    

class UserCreate(BaseModel):
    username : str =Field(min_length=3)
    password : str 

class JobMatchRequest(BaseModel):
        content : str = Field(min_length=10)
        job_description: str = Field(min_length=10)
