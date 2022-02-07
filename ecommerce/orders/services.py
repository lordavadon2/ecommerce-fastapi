from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from ecommerce.cart import models as cart_models
from ecommerce.orders import models, schema
from ecommerce.orders.mail import send_email_background
from ecommerce.user import models as user_models


async def initiate_order(background_tasks: BackgroundTasks, db_session: Session) -> models.Order:
    user_info = db_session.query(user_models.User).filter(user_models.User.email == "user@example.com").first()
    cart = db_session.query(cart_models.Cart).filter(cart_models.Cart.user_id == user_info.id).first()

    cart_items_objects = db_session.query(cart_models.CartItems).filter(cart_models.Cart.id == cart.id)
    if not cart_items_objects.count():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Items found in Cart !")

    total_amount: float = 0.0
    for item in cart_items_objects:
        total_amount += item.products.price

    new_order = models.Order(order_amount=total_amount,
                             shipping_address="Baker str., 587, London",
                             customer_id=user_info.id)
    db_session.add(new_order)
    db_session.commit()
    db_session.refresh(new_order)

    bulk_order_details_objects = list()
    for item in cart_items_objects:
        new_order_details = models.OrderDetails(order_id=new_order.id,
                                                product_id=item.products.id)
        bulk_order_details_objects.append(new_order_details)

    db_session.bulk_save_objects(bulk_order_details_objects)
    db_session.commit()

    # Send Email
    send_email_background(background_tasks, 'example@gmail.com', schema.ShowOrder.from_orm(new_order))

    # clear items in cart once new order is placed
    db_session.query(cart_models.CartItems).filter(cart_models.CartItems.cart_id == cart.id).delete()
    db_session.commit()

    return new_order


async def get_order_listing(db_session: Session) -> List[models.Order]:
    user_info = db_session.query(user_models.User).filter(user_models.User.email == "user@example.com").first()
    return db_session.query(models.Order).filter(models.Order.customer_id == user_info.id).all()
