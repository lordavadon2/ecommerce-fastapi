from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from ecommerce import db
from ecommerce.products import schema, services, models, validator

category_router = APIRouter(tags=['Categories'], prefix='/categories')
product_router = APIRouter(tags=['Products'], prefix='/products')


@category_router.post('/create',
             status_code=status.HTTP_201_CREATED,
             response_model=schema.DisplayCategory)
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


@category_router.get('/all', response_model=List[schema.DisplayCategory])
async def get_all_categories(database: Session = Depends(db.get_db)) -> List[models.Category]:
    return await services.get_all_categories(database)


@category_router.get('/{category_id}', response_model=schema.DisplayCategory)
async def get_category_by_id(category_id: int, database: Session = Depends(db.get_db)) -> models.Category:
    return await services.get_category_by_id(category_id, database)


@category_router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_category_by_id(category_id, database)


@product_router.post('/create', status_code=status.HTTP_201_CREATED,
             response_model=schema.ProductBase)
async def create_product(request: schema.Product, database: Session = Depends(db.get_db)) -> models.Product:
    category = await validator.verify_category_exist_by_id(request.category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )

    product = await services.create_product(request, database)
    return product


@product_router.get('/all', response_model=List[schema.ProductListing])
async def get_all_products(database: Session = Depends(db.get_db)) -> List[models.Product]:
    return await services.get_all_products(database)


@product_router.get('/{product_id}', response_model=schema.ProductListing)
async def get_product_by_id(product_id: int, database: Session = Depends(db.get_db)) -> models.Product:
    return await services.get_product_by_id(product_id, database)


@product_router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_product_by_id(product_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_product_by_id(product_id, database)
