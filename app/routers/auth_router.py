 
from datetime import timedelta
from fastapi import APIRouter, Depends

from app.core.security import create_access_token,  has_permission, permission_dependency
from app.schemas.auth_schema import LoginRequestSchema, LoginResponseSchema
from app.utils.common import ResponseSchema


routerAuth = APIRouter(
    prefix="/auth", tags=["Auth"],
   # dependencies=[Depends(is_autenticated)]
    )

@routerAuth.post("/login",response_model=ResponseSchema[LoginResponseSchema])
async def login(login_request: LoginRequestSchema):
    access_token = create_access_token(data={"sub": "user123", "exp": 1703980780,"permissions":["admin"]}, expires_token=50)
    print(access_token)
    return ResponseSchema({"access_token": access_token, "token_type": "bearer"})

@routerAuth.get("/me")
async def read_users_me(user=Depends(permission_dependency("admin"))):
    print(user)
    return ResponseSchema(data={"email": ""})