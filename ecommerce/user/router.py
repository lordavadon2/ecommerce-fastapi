from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ecommerce import db
from ecommerce.user import schema, validator, services, models

router = APIRouter(tags=['User'], prefix='/user')


@router.post('/registration',
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
