from fastapi import FastAPI
from routes import auth, resume, ai

app = FastAPI()

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(ai.router)






