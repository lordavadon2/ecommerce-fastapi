from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ecommerce.cart import models, schema


async def create_category(request: schema.Category, db_session: Session) -> models.Category:
    new_category = models.Category(**request.dict())
    db_session.add(new_category)
    db_session.commit()
    db_session.refresh(new_category)
    return new_category


async def get_all_categories(db_session: Session) -> List[models.Category]:
    return db_session.query(models.Category).all()


async def get_category_by_id(category_id: int, db_session: Session) -> models.Category:
    category_info = db_session.query(models.Category).get(category_id)
    if not category_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found!")
    return category_info


async def delete_category_by_id(category_id: int, db_session: Session):
    db_session.query(models.Category).filter(models.Category.id == category_id).delete()
    db_session.commit()


async def create_product(request: schema.Product, db_session: Session) -> models.Product:
    new_product = models.Product(**request.dict())
    db_session.add(new_product)
    db_session.commit()
    db_session.refresh(new_product)
    return new_product


async def get_all_products(db_session: Session) -> List[models.Product]:
    return db_session.query(models.Product).all()


async def get_product_by_id(product_id: int, db_session: Session) -> models.Product:
    product_info = db_session.query(models.Product).get(product_id)
    if not product_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
    return product_info


async def delete_product_by_id(product_id: int, db_session: Session):
    db_session.query(models.Product).filter(models.Product.id == product_id).delete()
    db_session.commit()
