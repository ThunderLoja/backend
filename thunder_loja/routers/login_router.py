from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Data
class ColabData(BaseModel):
    id: int
    password: str


# Router
router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get(colab_data: ColabData):
    if colab_data.id == 1 and colab_data.password == "42":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Login failed")