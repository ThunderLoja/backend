from fastapi import APIRouter
from pydantic import BaseModel


# Data
class SaleData(BaseModel):
    transaction_id: int
    client_cpf: int
    colab_id: int


# Router
router = APIRouter(
    prefix="/venda",
    tags=["venda"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{transaction_id}")
async def get(transaction_id: int):
    return {"message": f"Hello Venda {transaction_id}"}


@router.post("/")
async def post(sale_data: SaleData):
    return {"message": f"Hello Venda {sale_data.transaction_id}"}


@router.put("/")
async def put(sale_data: SaleData):
    return {"message": f"Hello Venda {sale_data.transaction_id}"}