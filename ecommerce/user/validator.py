from __future__ import annotations

from sqlalchemy.orm import Session

from ecommerce.user import models


async def verify_email_exist(email: str, db_session: Session) -> bool | None:
    return db_session.query(models.User).filter(models.User.email == email).first()
