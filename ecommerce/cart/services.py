from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ecommerce.cart import models, schema
from ecommerce.products import models as product_models
from ecommerce.user import models as user_models


async def add_items(cart_id: int, product_id: int, db_session: Session) -> models.CartItems:
    cart_item = models.CartItems(cart_id=cart_id, product_id=product_id)
    db_session.add(cart_item)
    db_session.commit()
    db_session.refresh(cart_item)
    return cart_item


async def add_to_cart(product_id: int, db_session: Session) -> dict:
    product_info = db_session.query(product_models.Product).get(product_id)
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found!")
    if product_info.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Out of Stock!")
    user_info = db_session.query(user_models.User).filter(user_models.User.email == 'user@example.com').first()
    cart_info = db_session.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()
    if not cart_info:
        new_cart = models.Cart(user_id=user_info.id)
        db_session.add(new_cart)
        db_session.commit()
        db_session.refresh(new_cart)
        await add_items(new_cart.id, product_info.id, db_session)
    else:
        await add_items(cart_info.id, product_info.id, db_session)
    return {"status": "Item Added to Cart"}


async def get_all_items(db_session: Session) -> schema.ShowCart:
    user_info = db_session.query(user_models.User).filter(user_models.User.email == 'user@example.com').first()
    return db_session.query(models.Cart).filter(models.Cart.user_id == user_info.id).first()


async def remove_cart_item(cart_item_id: int, db_session: Session) -> None:
    user_info = db_session.query(user_models.User).filter(user_models.User.email == "user@example.com").first()
    cart_id = db_session.query(models.Cart).filter(user_models.User.id == user_info.id).first()
    db_session.query(models.CartItems).filter(
        and_(models.CartItems.id == cart_item_id, models.CartItems.cart_id == cart_id.id)).delete()
    db_session.commit()
