from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from functools import wraps
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from app.core.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM

bearer = HTTPBearer()

def create_access_token(data: dict, expires_token: int = None):
    """Crea un token JWT con datos de usuario."""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() +  timedelta(minutes=expires_token or int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Error creating access token")

def decode_access_token(token: HTTPBearer):
    """Decodifica un token JWT."""
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def has_permission(permission:str,token: HTTPBearer):
    payload = decode_access_token(token)
    if permission not in payload.get("permissions", []):
        raise HTTPException("no tiene  acceso")  # Validar permisos
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

def is_autenticated(token: HTTPBearer = Depends(bearer)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

def permission_dependency(permission: str):
    def dependency(token: HTTPBearer = Depends(bearer)):
        has_permission(permission, token)  # Llama tu función
    return dependency