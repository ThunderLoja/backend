from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from thunder_loja.db_handler import DBHandler
from thunder_loja.routers.common_data import ColabData


# Router
router = APIRouter(
    prefix="/vendedor",
    tags=["vendedor"],
    responses={404: {"description": "Not found"}},
)

# Logger
logger = logging.getLogger('ClientRoute')


@router.get("/ativos")
async def get():
    sql = f"""
           SELECT colab_id, colab_nome, colab_cpf, colab_salario, colab_data_admi, colab_tipo, colab_ativo, colab_ger_id
           FROM colaborador
           WHERE colab_tipo = 2 and colab_ativo = B'1'
           """
    db_handler = DBHandler()

    sellers, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        seller_data = []
        
        for seller in sellers:
            seller_data.append(
                ColabData(
                    id=seller[0],
                    name=seller[1],
                    cpf=seller[2],
                    salary=seller[3],
                    admission_date=seller[4],
                    colab_type=seller[5],
                    is_active=seller[6],
                    manager_id=seller[7],
                    password="***"
                )
            )
            logger.debug(f"Seller: {seller}")
        
        return seller_data
    else:
        raise HTTPException(status_code=500, detail=error_msg)
        

@router.get("/{id}")
async def get(id: int):
    sql = f"""
           SELECT *
           FROM colaborador
           WHERE colab_id = {id}
           """
    db_handler = DBHandler()
    seller, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        if seller:
            seller_data = ColabData(
                            id=seller[0][0],
                            name=seller[0][1],
                            cpf=seller[0][2],
                            salary=seller[0][3],
                            admission_date=seller[0][4],
                            colab_type=seller[0][5],
                            is_active=seller[0][6],
                            manager_id=seller[0][7],
                            password="***")
    
            return seller_data
        else:
            raise HTTPException(status_code=404, detail="Client not found")
    else:
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/novo")
async def post(seller: ColabData):
    sql = f"""INSERT INTO colaborador(colab_id, colab_nome, colab_cpf, colab_salario, colab_data_admi, colab_tipo, colab_ativo, colab_ger_id, colab_senha)
                VALUES({seller.id}, '{seller.name}', {seller.cpf}, {seller.salary}, '{seller.admission_date}', 2, B'{int(seller.is_active)}', {seller.manager_id}, '{seller.password}');
            """
     
    db_handler = DBHandler()

    _, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        raise HTTPException(status_code=500, detail=error_msg)


@router.put("/atualizar")
async def put(seller: ColabData):
    sql = f"""
           UPDATE colaborador
            SET colab_nome = '{seller.name}',
                colab_cpf = {seller.cpf},
                colab_salario = {seller.salary},
                colab_data_admi = '{seller.admission_date}',
                colab_tipo = '{seller.colab_type}',
                colab_ativo = B'{int(seller.is_active)}',
                colab_ger_id = {seller.manager_id},
                colab_senha = '{seller.password}'
            WHERE colab_id = {seller.id}
            RETURNING colab_nome;
           """
    
    db_handler = DBHandler()

    seller, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        raise HTTPException(status_code=500, detail=error_msg)

    if not seller:
        raise HTTPException(status_code=404, detail="Client not found")