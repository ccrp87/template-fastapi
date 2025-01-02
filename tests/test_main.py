from datetime import datetime
import jwt

import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")  
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))  

def decode_access_token(token: str):
    """Decodifica un token JWT."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        print(e)
    except jwt.InvalidTokenError as e:
        print(e)

def create_access_token(data: dict):
    """Crea un token JWT con datos de usuario."""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        print(e)
token = create_access_token({"sub": "user123", "exp": 1703980780})
print(token)
print(decode_access_token(token))