from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce.db import db
from ecommerce.cart import schema, services

router = APIRouter(tags=['Cart'], prefix='/cart')


@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=schema.DisplayAddCart)
async def add_product_to_cart(product_id: int,
                              database: Session = Depends(db.get_db)) -> dict:
    return await services.add_to_cart(product_id, database)


@router.get('/all', response_model=schema.ShowCart)
async def get_all_cart_items(database: Session = Depends(db.get_db)) -> schema.ShowCart:
    return await services.get_all_items(database)


@router.delete('/{cart_item_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_cart_item_by_id(cart_item_id: int,
                                 database: Session = Depends(db.get_db)):
    await services.remove_cart_item(cart_item_id, database)
