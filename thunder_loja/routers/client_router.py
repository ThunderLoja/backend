from fastapi import APIRouter
from pydantic import BaseModel


# Data
class ClientData(BaseModel):
    name: str
    cpf: int


# Router
router = APIRouter(
    prefix="/cliente",
    tags=["cliente"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{cpf}")
async def get(cpf: int):
    return {"message": f"Hello Cliente {cpf}"}

