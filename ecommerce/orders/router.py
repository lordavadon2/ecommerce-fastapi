from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from ecommerce.auth.jwt import get_current_user
from ecommerce.db import db
from ecommerce.orders import schema, services, models
from ecommerce.user import schema as user_schema

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=schema.ShowOrder)
async def initiate_order_processing(background_tasks: BackgroundTasks, database: Session = Depends(db.get_db),
                                    current_user: user_schema.User = Depends(get_current_user)) -> models.Order:
    return await services.initiate_order(background_tasks, current_user, database)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schema.ShowOrder])
async def orders_list(database: Session = Depends(db.get_db),
                      current_user: user_schema.User = Depends(get_current_user)) -> List[models.Order]:
    return await services.get_order_listing(current_user, database)
