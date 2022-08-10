from pydantic import BaseModel
from uuid import UUID
import datetime


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    patronymic: str
    birthday: datetime.date
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserCreateRequest):
    email: str


class UserOut(BaseModel):
    id: int
    uuid: UUID
    email: str | None = None
    phone: str | None = None
    name: str
    surname: str
    patronymic: str
    birthday: datetime.date
    emailVerified: bool
    phoneVerified: bool
    createdAt: datetime.datetime
    lastLoginAt: datetime.datetime | None = None

    class Config:
        orm_mode = True


class ChangeUser(BaseModel):
    phone: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    birthday: datetime.date | None = None
    password: str | None = None

    class Config:
        orm_mode = True
