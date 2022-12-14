from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.db_models import User
from app.crud import user as user_crud
from app.schemas import user as user_schema, response as response_schema
from app.schemas.response import custom_errors
from app.utils import security
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("",
             summary="Registration user",
             response_model=response_schema.ResponseSuccess,
             status_code=201,
             responses={409: custom_errors("Conflict", [{"msg": "User with this email already exist"}])})
async def registration(user_data: user_schema.UserCreateRequest,
                       user_email: str = Depends(security.decode_email_token),
                       db: Session = Depends(get_db)):
    user = user_schema.UserCreate(**user_data.__dict__, email=user_email)
    new_user = user_crud.create_user(user=user, db=db)
    if not new_user:
        raise HTTPException(status_code=409, detail={"msg": "User with this email already exist"})
    return {"msg": "success"}


@router.get("/me", summary="Get Current User",
            response_model=user_schema.UserOut)
async def read_users_me(current_user: User = Depends(user_crud.get_current_user)):
    return current_user


@router.put("/me",
            summary="Change User Me",
            response_model=user_schema.UserOut,
            tags=[])
async def read_users_me(new_user_data: user_schema.ChangeUser,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(user_crud.get_current_user)):
    user_crud.change_user_data(user=current_user, user_data=new_user_data, db=db)
    return current_user
