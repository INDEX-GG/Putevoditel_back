from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    summary="Registration user",
    # response_model=response_schema.ResponseSuccess,
    # status_code=201,
    # responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}])}
)
async def registration():
    return {"msg": "users api"}
