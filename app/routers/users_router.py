from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserResponseSchema, UserRequestSchema
from app.services.user_service import UserService, get_user_service
from app.utils.common import ResponseSchema

routerUser = APIRouter(prefix="/users", tags=["Users"])


@routerUser.post(
    "/",
    response_model=ResponseSchema[UserResponseSchema],
    status_code=HTTPStatus.CREATED,
)
async def create_user(
    user: UserRequestSchema, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.create_user(user_create=user)
    return  ResponseSchema(data=db_user)


@routerUser.get("/{user_id}", response_model=ResponseSchema[UserResponseSchema])
def read_user(user_id: int):
    db_user = UserService.get_user_by_id(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@routerUser.put("/{user_id}", response_model=ResponseSchema[List[UserResponseSchema]])
def update_user(user_id: int, user: UserRequestSchema):
    db_user = UserService.get_user_by_id(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserService.update_user(user_id=user_id, user=user)


@routerUser.delete("/{user_id}", response_model=UserResponseSchema)
def delete_user(user_id: int):
    return UserService.delete_user(user_id=user_id)
