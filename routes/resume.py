from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from models import Resume as ResumeModel
from schemas import Resume
from auth import get_current_user
from ai import analyze_resume_ai

router = APIRouter()

@router.post("/analyze")
def analyze(resume: Resume, user=Depends(get_current_user)):
    db = SessionLocal()

    result = analyze_resume_ai(resume.content)

    new_resume = ResumeModel(
        content=resume.content,
        skills=",".join(result.get("skills", [])),
        score=result.get("score", 0),
        experience=".".join(result.get("experience", "")),
        user_id=user.id
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    db.close()

    return {"status": "success", "data": result}


@router.get("/resumes")
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
@router.put("/resumes/{id}")
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
@router.delete("/resumes/{id}")
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