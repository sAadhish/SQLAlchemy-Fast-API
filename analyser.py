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


