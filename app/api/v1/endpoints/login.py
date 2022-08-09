from fastapi import APIRouter


router = APIRouter(prefix="/login", tags=["Login"])


@router.get(
    "",
    summary="Login",
    # response_model=response_schema.ResponseSuccess,
    # status_code=201,
    # responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}])}
)
async def registration():
    return {"msg": "login api"}
