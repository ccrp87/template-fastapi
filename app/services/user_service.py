from datetime import datetime
from hashlib import sha256
from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.exceptions import BusinessLogicException
from app.db.session import  get_session
from app.models.user_model import User
from app.schemas.user_schema import UserRequestSchema, UserResponseSchema
from sqlalchemy import select


class UserService:
    def __init__(self, db_session: get_session):
        self.db_session = db_session

    async def create_user(self, user_create: UserRequestSchema) -> User:
        user = user_create.model_validate(user_create.model_dump())
        db_user = await self.get_user_by_email(email=user.email)
        if db_user:
            raise BusinessLogicException(message="Email already registered")

        user = User(**user_create.dict())
        user.created_at = datetime.now()
        user.hashed_password=sha256(user_create.email.encode()).hexdigest()
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user
    

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self) -> List[User]:
        query = select(User)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def update_user(
        self, user_id: int, user_update: UserResponseSchema
    ) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if user:
            for field, value in user_update.dict(exclude_unset=True).items():
                setattr(user, field, value)
            await self.db_session.commit()
            await self.db_session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        db_user = self.get_user_by_id(user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await self.db_session.delete(db_user)
        await self.db_session.commit()
        return True

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User.email).where(User.email == email)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(db_session=session)
