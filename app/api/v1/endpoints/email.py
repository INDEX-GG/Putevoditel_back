from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException
from app.api.dependencies import get_db
from app.schemas import response as response_schema
from app.schemas.response import custom_errors
from app.crud import user as user_crud, email_message as email_message_crud
from app.utils import email_sending


router = APIRouter(prefix="/email", tags=["Email"])


@router.get("/checkRegistration/{email}",
            summary="Check Email Registration",
            response_model=response_schema.ResponseCheckEmailRegistration)
async def check_email_registration(email: str = Path(),
                                   db: Session = Depends(get_db)):
    if user_crud.get_user_by_email(db=db, email=email.lstrip().rstrip()):
        return response_schema.ResponseCheckEmailRegistration(emailRegistration=True)
    return response_schema.ResponseCheckEmailRegistration(emailRegistration=False)


@router.get("/sendVerificationCode/{email}", summary="Call to phone",
            response_model=response_schema.ResponseSuccess,
            responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}]),
                       400: custom_errors("Bad Request", [{"msg": "usage limit exceeded"},
                                                          {"msg": "hardware or services problems"}])})
async def call_phone(email: str = Path(),
                     db: Session = Depends(get_db)):

    code = "123456"
    sending = email_sending.send_email_message(to_addr=email,
                                               html_template=email_sending.get_code_html_template(code),
                                               subject="Подтверждение почтового адреса ")

    if not sending:
        raise HTTPException(status_code=400, detail={"msg": "hardware or services problems"})
    email_message_crud.create_message(email=email, verification_code=code, db=db)
    return {"msg": "success"}
