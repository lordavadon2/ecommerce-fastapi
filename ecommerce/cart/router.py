from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce.db import db
from ecommerce.cart import schema, services, models

router = APIRouter(tags=['Cart'], prefix='/cart')


# @router.post('/create',
#              status_code=status.HTTP_201_CREATED,
#              response_model=schema.DisplayCategory)
# async def create_category(request: schema.Category,
#                           database: Session = Depends(db.get_db)) -> models.Category:
#     category = await validator.verify_category_exist(request.name, database)
#     if category:
#         raise HTTPException(
#             status_code=400,
#             detail='The category with this name already exists.'
#         )
#     new_category = await services.create_category(request, database)
#     return new_category
#
#
# @router.get('/all', response_model=List[schema.DisplayCategory])
# async def get_all_categories(database: Session = Depends(db.get_db)) -> List[models.Category]:
#     return await services.get_all_categories(database)
#
#
# @router.get('/{category_id}', response_model=schema.DisplayCategory)
# async def get_category_by_id(category_id: int, database: Session = Depends(db.get_db)) -> models.Category:
#     return await services.get_category_by_id(category_id, database)
#
#
# @router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
# async def delete_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
#     return await services.delete_category_by_id(category_id, database)


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
