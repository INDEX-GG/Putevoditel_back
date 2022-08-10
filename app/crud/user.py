from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.db_models import User
from app.schemas import user as user_schema
import uuid
import datetime
from app.utils import security
from app.api import dependencies


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate):
    if get_user_by_email(db=db, email=user.email):
        return False
    db_user = User(uuid=uuid.uuid4(),
                   email=user.email,
                   emailVerified=False,
                   phoneVerified=False,
                   password=security.hash_password(user.password),
                   name=user.name,
                   surname=user.surname,
                   patronymic=user.patronymic,
                   birthday=user.birthday,
                   createdAt=datetime.datetime.utcnow())
    db.add(db_user)
    db.commit()
    return True


def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_current_user(db: Session = Depends(dependencies.get_db),
                     access_token: str = Depends(dependencies.oauth2_scheme)):
    token_data = security.decode_access_token(access_token)
    user_id = token_data.get("sub")
    user: User = get_user_by_id(db=db, user_id=user_id)
    if not User:
        raise security.credentials_exception
    return user
