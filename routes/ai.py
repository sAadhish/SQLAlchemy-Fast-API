from fastapi import APIRouter, Depends, HTTPException
from schemas import JobMatchRequest,MultiJobMatchRequest
from auth import get_current_user
from ai import matching_job
from analyser import match_multiple_jobs,recommend_jobs_from_history
from database import SessionLocal
from models import JobMatch

router = APIRouter()

@router.post("/compare")
def compare(data: JobMatchRequest, user=Depends(get_current_user)):
    try:
        result = matching_job(data.content, data.job_description)

        return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/match-multiple")
def match_multiple(data : MultiJobMatchRequest,user=Depends(get_current_user)):
    try:
        db=SessionLocal()

        result = match_multiple_jobs(data.content,data.job_description)
        for r in result:
            new_match=JobMatch(
                user_id = user.id,
                job = r["job"],
                score = r["score"],
                fit = r["fit"],
            )
            db.add(new_match)

        db.commit()
        db.close()


        return{"status":"success","data":result}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/recommend")
def recommend(user=Depends(get_current_user)):

    db=SessionLocal()
    matches=db.query(JobMatch).filter(JobMatch.user_id ==user.id).all()
    db.close()

    result=recommend_jobs_from_history(matches)

    return{
        "status": "success",
        "recommendations": result
    }