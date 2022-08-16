from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException
from app.api.dependencies import get_db
from app.schemas import response as response_schema
from app.schemas.response import custom_errors
from app.crud import user as user_crud, email_message as email_message_crud
from app.utils import email_sending, security


router = APIRouter(prefix="/email", tags=["Email"])


@router.get("/checkRegistration/{email}",
            summary="Check Email Registration",
            response_model=response_schema.ResponseCheckEmailRegistration)
async def check_email_registration(email: str = Path(),
                                   db: Session = Depends(get_db)):
    if user_crud.get_user_by_email(db=db, email=email.lstrip().rstrip()):
        return response_schema.ResponseCheckEmailRegistration(emailRegistration=True)
    return response_schema.ResponseCheckEmailRegistration(emailRegistration=False)


@router.get("/sendVerificationCode/{email}",
            summary="Call to phone",
            response_model=response_schema.ResponseSuccess,
            responses={409: custom_errors("Conflict", [{"msg": "User with this email already exist"}]),
                       400: custom_errors("Bad Request", [{"msg": "Usage limit exceeded"},
                                                          {"msg": "Hardware or services problems"}])})
async def send_email(email: str = Path(),
                     db: Session = Depends(get_db)):
    check_count_of_calls = email_message_crud.check_count_of_messages(email=email, max_count_of_calls_in_period=10,
                                                                      time_period_in_minutes=30, db=db)
    if not check_count_of_calls:
        raise HTTPException(status_code=400, detail={"msg": "usage limit exceeded"})
    code = email_sending.generate_code()
    sending = email_sending.send_email_message(to_addr=email,
                                               html_template=email_sending.get_code_html_template(code),
                                               subject="Подтверждение почтового адреса ")
    if not sending:
        raise HTTPException(status_code=400, detail={"msg": "Hardware or services problems"})
    email_message_crud.create_message(email=email, verification_code=code, db=db)
    return {"msg": "success"}


@router.get("/check_verification_code/{email}/{code}",
            summary="Check Verification Code",
            response_model=response_schema.EmailToken,
            responses={400: custom_errors("Bad Request", [{"msg": "number of attempts exceeded"},
                                                          {"msg": "wrong verification code"}])
                       })
async def check_verification_code(email: str = Path(),
                                  code: str = Path(),
                                  db: Session = Depends(get_db)):
    check_unsuccessful_try = email_message_crud.check_count_of_unsuccessful_try_verif_code(db=db, email=email)
    if not check_unsuccessful_try:
        raise HTTPException(status_code=400, detail={"msg": "number of attempts exceeded"})
    check_verif_code = email_message_crud.check_verification_code(db=db, email=email, verification_code=code)
    if not check_verif_code:
        raise HTTPException(status_code=400, detail={"msg": "wrong verification code"})
    email_token = security.create_email_token(data={"sub": email})
    return response_schema.EmailToken(emailToken=email_token)
