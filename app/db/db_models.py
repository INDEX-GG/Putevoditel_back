from sqlalchemy import Column, String, TIMESTAMP, BOOLEAN, BigInteger
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    email = Column("email", String, unique=True)
    emailVerified = Column("email_verified", BOOLEAN, nullable=False)
    phone = Column("phone", String, unique=True)
    phoneVerified = Column("phone_verified", BOOLEAN, nullable=False)
    password = Column("password", String)
    name = Column("name", String)
    surname = Column("surname", String)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)
    lastLoginAt = Column("last_login_at", TIMESTAMP)
    deletedAt = Column("deleted_at", TIMESTAMP)
    emailVerifiedAt = Column("email_verified_at", TIMESTAMP)
