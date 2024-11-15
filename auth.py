# Authentication
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context from Cryptcontext

# For hasing password
pwd_context = Cryptcontext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT
SECRET_KEY = ""
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = ""

#Hash Password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify Password
def verify_password(plain_password: str, hased_password: str):
    return pwd_context.verify(plain_password, hased_password)

# JWT Token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)
    return encoded_jwt

# JWT token verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None

