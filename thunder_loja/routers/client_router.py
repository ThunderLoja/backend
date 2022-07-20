from fastapi import APIRouter
from pydantic import BaseModel


# Data
class ClientData(BaseModel):
    cpf: int
    name: str


# Router
router = APIRouter(
    prefix="/cliente",
    tags=["cliente"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{cpf}")
async def get(cpf: int):
    return {"message": f"Hello Cliente {cpf}"}


@router.post("/")
async def post(client: ClientData):
    return {"message": f"Hello Cliente {client.name}"}


@router.put("/")
async def put(client: ClientData):
    return {"message": f"Hello Cliente {client.name}"}