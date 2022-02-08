from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce.auth.jwt import get_current_user
from ecommerce.db import db
from ecommerce.products import schema, services, models, validator


router = APIRouter(tags=['Products'], prefix='/products')


@router.post('/category/create',
                      status_code=status.HTTP_201_CREATED,
                      response_model=schema.DisplayCategory,
                      dependencies=[Depends(get_current_user)])
async def create_category(request: schema.Category,
                          database: Session = Depends(db.get_db)) -> models.Category:
    category = await validator.verify_category_exist(request.name, database)
    if category:
        raise HTTPException(
            status_code=400,
            detail='The category with this name already exists.'
        )
    new_category = await services.create_category(request, database)
    return new_category


@router.get('/category/all', response_model=List[schema.DisplayCategory])
async def get_all_categories(database: Session = Depends(db.get_db)) -> List[models.Category]:
    return await services.get_all_categories(database)


@router.get('/category/{category_id}', response_model=schema.DisplayCategory)
async def get_category_by_id(category_id: int, database: Session = Depends(db.get_db)) -> models.Category:
    return await services.get_category_by_id(category_id, database)


@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
                        dependencies=[Depends(get_current_user)])
async def delete_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_category_by_id(category_id, database)


@router.post('/create', status_code=status.HTTP_201_CREATED,
                     response_model=schema.ProductBase, dependencies=[Depends(get_current_user)])
async def create_product(request: schema.Product, database: Session = Depends(db.get_db)) -> models.Product:
    category = await validator.verify_category_exist_by_id(request.category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )

    product = await services.create_product(request, database)
    return product


@router.get('/all', response_model=List[schema.ProductListing])
async def get_all_products(database: Session = Depends(db.get_db)) -> List[models.Product]:
    return await services.get_all_products(database)


@router.get('/{product_id}', response_model=schema.ProductListing)
async def get_product_by_id(product_id: int, database: Session = Depends(db.get_db)) -> models.Product:
    return await services.get_product_by_id(product_id, database)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
                       dependencies=[Depends(get_current_user)])
async def delete_product_by_id(product_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_product_by_id(product_id, database)
