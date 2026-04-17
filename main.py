from fastapi import FastAPI, HTTPException
from models import Resume as ResumeModel
from analyser import analyser
from database import SessionLocal
from validate import Resume
import logging


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#------- POST -------
@app.post("/analyze")
def analyze(resume: Resume):
    try:
        logger.info("Received resume for analysis")

        result = analyser(resume.content)

        db = SessionLocal()

        new_resume = ResumeModel(
            content=resume.content,
            skills=",".join(result["Skills"]),
            score=result["score"],
            experience=result["Experience"]
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
def get_resumes():
    db = SessionLocal()
    resumes = db.query(ResumeModel).all()
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
def update_resume(id: int, score: int):
    db = SessionLocal()
    resume = db.query(ResumeModel).filter(ResumeModel.id == id).first()

    if not resume:
        db.close()
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.score = score
    db.commit()
    db.close()

    return {"message": "Resume updated"}

#------- DELETE -------
@app.delete("/resumes/{id}")
def delete_resume(id: int):
    db = SessionLocal()
    resume = db.query(ResumeModel).filter(ResumeModel.id == id).first()

    if not resume:
        db.close()
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()
    db.close()

    return {"message": "Resume deleted"}