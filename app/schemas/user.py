from pydantic import BaseModel
from typing import Literal
from uuid import UUID
import datetime


class UserCreateRequest(BaseModel):
    name: str | None
    surname: str | None
    patronymic: str | None
    birthday: datetime.date | None
    phone: str | None = None
    passport: str | None = None
    address: str | None = None
    familyComposition: str | None = None
    gender: Literal["male", "female"] | None = None
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserCreateRequest):
    email: str


class UserOut(BaseModel):
    id: int
    uuid: UUID
    email: str
    phone: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    birthday: datetime.date | None = None
    passport: str | None = None
    address: str | None = None
    familyComposition: str | None = None
    gender: Literal["male", "female"] | None = None
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
