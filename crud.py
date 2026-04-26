'''

from fastapi import FastAPI, HTTPException
from database import SessionLocal
from models import User
from schemas import UserCreate
from auth import hash_password

#app = FastAPI()

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


# ------------- GET ----------

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

'''