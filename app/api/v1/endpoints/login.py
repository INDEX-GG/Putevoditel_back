from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import response as response_schema
from app.schemas.response import custom_errors
from app.utils import security


router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/login",
             summary="OAuth2 Login",
             response_model=response_schema.ResponseLogin,
             responses={400: custom_errors("Bad Request", [{"msg": "Incorrect username or password"}])})
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail={"msg": "Incorrect username or password"})
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token}


@router.post("/reset-password", summary="Recovery password by email",
             response_model=response_schema.ResponseSuccess,
             responses={400: custom_errors("Conflict", [{"msg": "user with this phone does not exist"}])})
async def reset_password(user_email: str = Depends(security.decode_email_token),
                         new_password: str = Body(embed=True),
                         db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(status_code=400, detail={"msg": "user with this phone does not exist"})
    crud_user.change_user_password(db=db, user=user, new_password=security.hash_password(new_password))
    return {"msg": "success"}
