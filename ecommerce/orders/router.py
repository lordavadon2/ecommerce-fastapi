from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce.db import db
from ecommerce.orders import schema, services, models

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=schema.ShowOrder)
async def initiate_order_processing(database: Session = Depends(db.get_db)) -> models.Order:
    return await services.initiate_order(database)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schema.ShowOrder])
async def orders_list(database: Session = Depends(db.get_db)) -> List[models.Order]:
    return await services.get_order_listing(database)
