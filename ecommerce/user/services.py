from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ecommerce.user import models, schema


async def create_user(request: schema.User, db_session: Session) -> models.User:
    new_user = models.User(**request.dict())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user


async def get_all_users(db_session: Session) -> List[models.User]:
    return db_session.query(models.User).all()


async def get_user_by_id(user_id: int, db_session: Session) -> models.User:
    user_info = db_session.query(models.User).get(user_id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found!")
    return user_info


async def delete_user_by_id(user_id: int, db_session: Session):
    db_session.query(models.User).filter(models.User.id == user_id).delete()
    db_session.commit()
