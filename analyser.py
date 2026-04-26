from ai import matching_job

def analyser(text):
    text = text.lower()
    skills = ["python", "sql", "excel", "machine learning", "ai"]
    found_skill =[]
    experience_keywords = ["intern", "worked", "developed", "project"]
    found_experience_level = []

    for skill in skills:
        if skill in text:
            found_skill.append(skill)

    score=len(found_skill)

    for experience in experience_keywords:
        if experience in text:
            found_experience_level.append(experience)

    return{
        "Skills" : found_skill,
        "Score":score,
        "Experience":found_experience_level
                }


def match_multiple_jobs(content : str,job_description:list):
    results=[]
    for job in job_description:
        result=matching_job(content,job_description)

        if "match_score" in result:
            results.append({
                "job": job,
                "score": result["match_score"],
                "fit": result["fit"],
                "missing_skills": result["missing_skills"]
            })
    results.sort(key=lambda x:x["score"] ,reverse=True)
    
    return results


#  Recommendation Logic
def recommend_jobs_from_history(matches):
    top_matches = sorted(matches,key=lambda x:x.score,reverse=True)[:3]

    return [
        {
            "Job":m.job,
            "Reason":"Based on your previous high match scores"
        }
        for m in top_matches
    ]