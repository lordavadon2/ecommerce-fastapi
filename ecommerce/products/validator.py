from __future__ import annotations

from sqlalchemy.orm import Session

from ecommerce.products import models


async def verify_category_exist(name: str, db_session: Session) -> models.Category | None:
    return db_session.query(models.Category).filter(models.Category.name == name).first()


async def verify_category_exist_by_id(category_id: int, db_session: Session) -> models.Category | None:
    return db_session.query(models.Category).filter(models.Category.id == category_id).first()
