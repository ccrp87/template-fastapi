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

def decode_access_token(token: str):
    """Decodifica un token JWT."""
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

async def is_autenticated(request: Request, token: str = Depends(bearer)):
    payload = decode_access_token(token)
    request.state.user = payload
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

def get_current_user(request: Request):
    if "user" not in request.state:
        raise HTTPException(status_code=401, detail="User not found")
    return request.state.user

def allow_anonymous(request: Request=None):
    request.state.user = None
    request.state.is_anonymous = True
def permission_required(permission: str,request: Request=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = request.state.user
            print(user)
            # Usamos Depends para inyectar el usuario y verificar los permisos
            user = kwargs.get("current_user")
            if user is None:
                raise HTTPException(status_code=401, detail="User not found")
            
            # Verificamos si el usuario tiene el permiso
            if permission not in user["permissions"]:
                raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
            
            # Si tiene el permiso, ejecutamos la función del endpoint
            return await func(*args, **kwargs)
        return wrapper
    return decorator