from pydantic import BaseModel,Field

class Resume(BaseModel):
    content : str = Field(min_length=20)

