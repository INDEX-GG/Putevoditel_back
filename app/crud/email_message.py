from sqlalchemy.orm import Session
import datetime
from app.db.db_models import EmailMessages, EmailVerifyUnsuccessfulTry


def create_message(db: Session, email: str, verification_code: str):
    db_message = EmailMessages(email=email,
                               emailValidate=False,
                               validateCode=verification_code,
                               createdAt=datetime.datetime.utcnow())
    db.add(db_message)
    db.commit()


def check_count_of_messages(db: Session, email: str, max_count_of_calls_in_period: int = 3,
                            time_period_in_minutes: int = 30):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_calls = db.query(EmailMessages).filter(EmailMessages.email == email, EmailMessages.createdAt >= time_limit).all()
    if len(db_calls) >= max_count_of_calls_in_period:
        return False
    return True


def check_verification_code(db: Session, email: str, verification_code: str, time_period_in_minutes: int = 5):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_message = db.query(EmailMessages)\
        .filter(EmailMessages.email == email, EmailMessages.createdAt >= time_limit)\
        .order_by(EmailMessages.createdAt.desc()).first()
    if not db_message:
        create_unsuccessful_try_record(db=db, email=email)
        return False
    if db_message.emailValidate:
        return False
    if verification_code != db_message.validateCode:
        create_unsuccessful_try_record(db=db, email=email)
        return False
    db_message.emailValidate = True
    db.commit()
    return True


def create_unsuccessful_try_record(db: Session, email: str):
    db_spam_record = EmailVerifyUnsuccessfulTry(email=email, createdAt=datetime.datetime.utcnow())
    db.add(db_spam_record)
    db.commit()


def check_count_of_unsuccessful_try_verif_code(db: Session, email: str,
                                               max_count_of_unsuccessful_try_in_period: int = 5,
                                               time_period_in_minutes: int = 5):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_try = db.query(EmailVerifyUnsuccessfulTry).filter(EmailMessages.email == email,
                                                         EmailVerifyUnsuccessfulTry.createdAt >= time_limit).all()
    if len(db_try) >= max_count_of_unsuccessful_try_in_period:
        return False
    return True
