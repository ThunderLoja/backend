import logging
from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from thunder_loja.db_handler import DBHandler


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


# Logger
logger = logging.getLogger('SaleRoute')


@router.get("/relatorio")
async def get(q: Union[str, None] = None):
    # Join 
    return {"message": f"Hello Relatorio de Venda"}


@router.post("/nova")
async def post(sale_data: SaleData):
    # Dados do json: transação, venda, [(prod_id, quant)...]
    # Criar nova linha em transacao
    # Criar nova linha em venda
    # Iterar pelo array, subtraindo a quantidade do produto e adicionando cada linha a prod_venda
    # Commit
    return {"message": f"Hello Venda {sale_data.transaction_id}"}
