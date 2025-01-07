 
from datetime import timedelta
from fastapi import APIRouter, Depends

from app.core.security import create_access_token,  has_permission
from app.schemas.auth_schema import LoginRequestSchema, LoginResponseSchema
from app.utils.common import ResponseSchema
from app.core.config_open_api import doc_responses


routerAuth = APIRouter(
    prefix="/auth", tags=["Auth"],
    responses=doc_responses,
    )

@routerAuth.post("/login",response_model=ResponseSchema[LoginResponseSchema])
async def login(login_request: LoginRequestSchema):
    access_token = create_access_token(data={"user_name": "john","email":"john@localhost", "exp": 1703980780,"permissions":["admin"]}, expires_token=50)
    print(access_token)
    data:LoginResponseSchema = LoginResponseSchema(user_name="john",email="john@localhost", token= access_token)   
    return ResponseSchema(data=data)

@routerAuth.get("/me")
async def read_users_me(user=Depends(has_permission("admin"))):
    print(user)
    return ResponseSchema(data=user)