from google import genai
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume_ai(text : str):
    prompt = f"""
    Analyze this resume and respond ONLY in valid JSON format.
    Do NOT use markdown (no ```).
    Format:
    {{
      "skills": ["skill1", "skill2"],
      "experience": "beginner/intermediate/advanced",
      "score": number (0-100),
      "reason": "why this score",
      "suggestions": ["suggestion1", "suggestion2"]
    }}

    Resume : 
    {text}
    """ 

    response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=prompt
    )

    try:
        return json.loads(response.text)
    except:
        return {"error": "Invalid JSON from AI", "raw": response.text}
    


def matching_job(resume_text: str ,job_desc : str):
    prompt=f"""
    Compare the resume with the job description and respond ONLY in valid JSON format.
    Do NOT use markdown (no ```).

    Format:
    {{
      "match_score": number (0-100),
      "fit": "poor/good/excellent",
      "missing_skills": ["skill1", "skill2"],
      "reason": "short explanation",
      "suggestions": ["suggestion1", "suggestion2"]
    }}

    Resume:
    {resume_text}
    Job Description:
    {job_desc}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    #return print(response)
    try:
        return json.loads(response.text)
    except:
        return {"error": "Invalid JSON", "raw": response.text}
    


