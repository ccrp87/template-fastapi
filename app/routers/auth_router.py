 
from datetime import timedelta
from fastapi import APIRouter, Depends

from app.core.security import create_access_token, get_current_user, is_autenticated, permission_required
from app.schemas.auth_schema import LoginRequestSchema, LoginResponseSchema
from app.utils.common import ResponseSchema


routerAuth = APIRouter(prefix="/auth", tags=["Auth"],dependencies=[Depends(is_autenticated)])

@routerAuth.post("/login",response_model=ResponseSchema[LoginResponseSchema])
async def login(login_request: LoginRequestSchema):
    access_token = create_access_token(data={"sub": "user123", "exp": 1703980780}, expires_token=50)
    print(access_token)
    return ResponseSchema({"access_token": access_token, "token_type": "bearer"})

@routerAuth.get("/me")
@permission_required("admin")
async def read_users_me(user=Depends(get_current_user)):
    return ResponseSchema(data={"email": ""})