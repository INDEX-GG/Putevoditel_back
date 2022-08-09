from sqlalchemy.orm import Session
import datetime
from app.db.db_models import EmailMessages


def create_message(db: Session, email: str, verification_code: str):
    db_message = EmailMessages(email=email,
                               emailValidate=False,
                               validateCode=verification_code,
                               createdAt=datetime.datetime.utcnow())
    db.add(db_message)
    db.commit()
