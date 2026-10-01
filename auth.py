from jose import jwt, JWTError

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException,Depends

from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecret"

ALGORITHUM  ="HS256"

ACCESS_TOKEN_EXPIRE_TIME = 30

oauth2_schema  =OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHUM)

def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHUM)

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    