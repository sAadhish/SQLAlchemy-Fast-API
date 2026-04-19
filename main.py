from fastapi import FastAPI, HTTPException,Depends
from models import Resume as ResumeModel,User
from analyser import analyser
from database import SessionLocal
from schemas import Resume,UserCreate
import logging
from auth import hash_password,verify_password,create_access_token,get_current_user
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#------- POST -------
@app.post("/analyze")
def analyze(resume: Resume,user=Depends(get_current_user)):
    try:
        logger.info("Received resume for analysis")

        result = analyser(resume.content)

        db = SessionLocal()

        new_resume = ResumeModel(
            content=resume.content,
            skills=",".join(result["Skills"]),
            score=result["Score"],
            experience=result["Experience"],
            user_id =user.id
        )

        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
        db.close()

        logger.info(f"Stored resume with ID {new_resume.id}")

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


#------- GET -------
@app.get("/resumes")
def get_resumes(user=Depends(get_current_user)):
    db = SessionLocal()
    resumes = db.query(ResumeModel).filter(ResumeModel.user_id == user.id).all()
    db.close()

    result = []
    for r in resumes:
        result.append({
            "id": r.id,
            "content": r.content,
            "skills": r.skills,
            "score": r.score,
            "Experience":r.experience
        })

    return result


#------- PUT -------
@app.put("/resumes/{id}")
def update_resume(id: int, score: int,user = Depends(get_current_user)):
    db = SessionLocal()
    resume = db.query(ResumeModel).filter(ResumeModel.id == id,ResumeModel.user_id == user.id).first()

    if not resume:
        db.close()
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.score = score
    db.commit()
    db.close()

    return {"message": "Resume updated"}

#------- DELETE -------
@app.delete("/resumes/{id}")
def delete_resume(id: int,user = Depends(get_current_user)):
    db = SessionLocal()
    resume = db.query(ResumeModel).filter(ResumeModel.id == id,ResumeModel.user_id == user.id).first()

    if not resume:
        db.close()
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()
    db.close()

    return {"message": "Resume deleted"}


# ----- Register ----- POST -----

@app.post("/register")
def register(user : UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


# ------------- GET USERS----------

@app.get("/users")
def user_list():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username
        })

    return result

# ------- LOGIN --------

@app.post("/login")
def login(user : UserCreate):

    db=SessionLocal()

    db_user = db.query(User).filter(user.username == User.username).first()

    if not db_user:
        db.close()
        raise HTTPException(status_code=400,detail="User not found")
    
    if not verify_password(user.password,db_user.hashed_password):
        db.close()
        raise HTTPException(status_code=400,detail="User not found")
    
    db.close()

    token = create_access_token({"sub":db_user.username})

    return {"access_token": token}