# SQLAlchemy-Fast-API

## 🚀 Resume Analyzer API

A production-ready backend API built with FastAPI that analyzes resume text, extracts key skills, assigns a score, and stores results in a PostgreSQL database.

⸻

## 📌 Features
	•	🔍 Analyze resume content for key skills
	•	📊 Generate a skill-based score
	•	💾 Store results in PostgreSQL
	•	📥 Retrieve stored resumes
	•	✏️ Update resume scores
	•	❌ Delete resumes
	•	🧠 Built with clean architecture & ORM (SQLAlchemy)
	•	📜 Logging & error handling implemented

⸻

## 🛠️ Tech Stack
	•	Backend Framework: FastAPI
	•	Database: PostgreSQL
	•	ORM: SQLAlchemy
	•	Validation: Pydantic
	•	Server: Uvicorn

⸻

## 📂 Project Structure
    resume-analyzer/
    │
    ├── main.py          # FastAPI app (routes + logic)
    ├── analyzer.py      # Resume analysis logic
    ├── models.py        # ORM models
    ├── validate.py      # Pydantic
    ├── database.py      # DB connection setup
    ├── requirements.txt # Dependencies
    └── README.md        # Project documentation


## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
     git clone <your-repo-url>
     cd resume-analyzer
### 2️⃣ Create Virtual Environment
     python -m venv venv
     source venv/bin/activate   # Mac/Linux
     venv\Scripts\activate      # Windows
### 3️⃣ Install Dependencies
     pip install -r requirements.txt
### 4️⃣ Configure Database

Make sure PostgreSQL is running and create a database:

    CREATE DATABASE resume_db;
Update your database.py with credentials:
     
    DATABASE_URL = "postgresql://postgres:your_password@localhost/resume_db"

### 5️⃣ Run the Server
    uvicorn main:app --reload

## 📡 API Endpoints

###🔹 Analyze Resume (Create + Store)

    POST /analyze
    {
     "content": "I know Python, SQL, and Machine Learning"
    }


⸻

### 🔹 Get All Resumes

    GET /resumes

⸻

### 🔹 Update Resume Score

	PUT /resumes/{id}?score=5

⸻

### 🔹 Delete Resume

	DELETE /resumes/{id}

⸻

## 🧪 API Testing

	Open interactive docs: http://127.0.0.1:8000/docs

### 📊 Example Response

	{
 	 	"status": "success",
 	 	"data": {
    	"skills_found": ["python", "sql"],
    	"score": 2
  		}
	}
# 🔒 Error Handling
	•	Returns proper HTTP status codes
	•	Handles invalid input via Pydantic
	•	Logs errors for debugging

	
#👨‍💻 Author

## Aadhish S
