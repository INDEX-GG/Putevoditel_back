from sqlalchemy import Column, String, TIMESTAMP, BOOLEAN, BigInteger, DATE
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    emailVerified = Column("email_verified", BOOLEAN, nullable=False)
    phone = Column("phone", String)
    phoneVerified = Column("phone_verified", BOOLEAN, nullable=False)
    password = Column("password", String)
    name = Column("name", String)
    surname = Column("surname", String)
    patronymic = Column("patronymic", String)
    birthday = Column("birthday", DATE)
    passport = Column("passport", String)
    address = Column("address", String)
    familyComposition = Column("family_composition", String)
    gender = Column("gender", String)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)
    lastLoginAt = Column("last_login_at", TIMESTAMP)
    deletedAt = Column("deleted_at", TIMESTAMP)
    emailVerifiedAt = Column("email_verified_at", TIMESTAMP)
    phoneVerifiedAt = Column("phone_verified_at", TIMESTAMP)


class EmailMessages(Base):
    __tablename__ = "email_messages"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    email = Column("phone", String)
    validateCode = Column("validate_code", String)
    emailValidate = Column("email_validate", BOOLEAN, nullable=False)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)


class EmailVerifyUnsuccessfulTry(Base):
    __tablename__ = "email_verify_unsuccessful_try"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    email = Column("email", String)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
