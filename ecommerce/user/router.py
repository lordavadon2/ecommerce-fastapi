from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce import db
from ecommerce.user import schema, validator, services, models

router = APIRouter(tags=['User'], prefix='/users')


@router.post('/create',
             status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.User,
                                   database: Session = Depends(db.get_db)) -> models.User:
    user = await validator.verify_email_exist(request.email, database)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this email already exists.'
        )
    new_user = await services.create_user(request, database)
    return new_user


@router.get('/', response_model=List[schema.DisplayUser])
async def get_all_users(database: Session = Depends(db.get_db)) -> List[models.User]:
    return await services.get_all_users(database)


@router.get('/{user_id}', response_model=schema.DisplayUser)
async def get_all_users(user_id: int, database: Session = Depends(db.get_db)) -> models.User:
    return await services.get_user_by_id(user_id, database)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(user_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_user_by_id(user_id, database)
