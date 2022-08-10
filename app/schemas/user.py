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
    emailVerified: bool
    phoneVerified: bool
    createdAt: datetime.datetime
    phone: int | None = None
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    rating: int | None = None
    googleId: str | None = None
    vkId: str | None = None
    appleId: str | None = None
    updatedAt: datetime.datetime | None = None
    lastLoginAt: datetime.datetime | None = None
    deletedAt: datetime.datetime | None = None
    emailVerifiedAt: datetime.datetime | None = None
    phoneVerifiedAt: datetime.datetime | None = None

    class Config:
        orm_mode = True
