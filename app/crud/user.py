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
                   emailVerified=True,
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


def authenticate_user(db: Session, username: str, password: str):
    db_user: User = get_user_by_email(db=db, email=username)
    if not db_user:
        return False
    if not security.verify_password(password, db_user.password):
        return False
    db_user.lastLoginAt = datetime.datetime.utcnow()
    db.commit()
    return db_user


def change_user_password(db: Session, user: User, new_password: str):
    user.password = new_password
    db.commit()


def change_user_data(db: Session, user: User, user_data: user_schema.ChangeUser):
    if user_data.phone:
        user.phone = user_data.phone
    if user_data.name:
        user.name = user_data.name
    if user_data.surname:
        user.surname = user_data.surname
    if user_data.patronymic:
        user.patronymic = user_data.patronymic
    if user_data.birthday:
        user.birthday = user_data.birthday
    if user_data.password:
        user.password = security.hash_password(user_data.password)
    db.commit()
