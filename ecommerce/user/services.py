from sqlalchemy.orm import Session

from ecommerce.user import models, schema


async def create_user(request: schema.User, db_session: Session) -> models.User:
    new_user = models.User(**request.dict())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user
