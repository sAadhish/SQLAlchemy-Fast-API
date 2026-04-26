from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
#SECRET_KEY = "mysecretkey" 
ALGORITHM = "HS256"



pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


#create token
def create_access_token(data : dict):
    to_encode = data.copy()

    expire_date = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire_date})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return token

def verify_token(token: str):
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

#token reading
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username =payload.get("sub")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
