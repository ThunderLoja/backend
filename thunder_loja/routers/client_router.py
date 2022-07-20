from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from thunder_loja.db_handler import DBHandler


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

# Logger
logger = logging.getLogger('ClientRoute')


@router.get("/todos")
async def get():
    sql = f"""
           SELECT *
           FROM cliente
           """
    db_handler = DBHandler()

    clients, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        client_data = []
        
        for client in clients:
            client_data.append(ClientData(cpf=client[0], name=client[1]))
            logger.debug(f"Cliente: {client}")
        
        return client_data
    else:
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/{cpf}")
async def get(cpf: int):
    sql = f"""
           SELECT *
           FROM cliente
           WHERE clt_cpf = {cpf}
           """
    db_handler = DBHandler()
    client, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        if client:
            client_data = ClientData(cpf=client[0][0], name=client[0][1])
    
            return client_data
        else:
            raise HTTPException(status_code=404, detail="Client not found")
    else:
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/novo")
async def post(client: ClientData):
    sql = f"""
           INSERT INTO cliente(clt_cpf, clt_nome)
            VALUES({client.cpf}, '{client.name}');
           """
    
    db_handler = DBHandler()

    _, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        raise HTTPException(status_code=500, detail=error_msg)


@router.put("/atualizar")
async def put(client: ClientData):
    sql = f"""
           UPDATE cliente
            SET clt_nome ='{client.name}'
            WHERE clt_cpf = '{client.cpf}'
            RETURNING clt_nome;
           """
    
    db_handler = DBHandler()

    client, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        raise HTTPException(status_code=500, detail=error_msg)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")