from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from thunder_loja.db_handler import DBHandler
from thunder_loja.routers.common_data import ColabData


# Data
class ColabLoginData(BaseModel):
    id: int
    password: str


# Router
router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

# Logger
logger = logging.getLogger('LoginRoute')


@router.put("/")
async def get(colab_data: ColabLoginData):
    sql = f"""
           SELECT colab_id, colab_nome, colab_cpf, colab_salario, colab_data_admi, colab_tipo, colab_ativo, colab_ger_id
           FROM colaborador
           WHERE colab_id = {colab_data.id} and colab_senha = '{colab_data.password}' and colab_ativo = B'1'
           """
    db_handler = DBHandler()
    colaborator = db_handler.send_command(sql)

    if colaborator is not None:
        if colaborator:
            logger.debug(colaborator)

            colab_data = ColabData(
                id=colaborator[0][0],
                name=colaborator[0][1],
                cpf=colaborator[0][2],
                salary=colaborator[0][3],
                admission_date=colaborator[0][4],
                colab_type=colaborator[0][5],
                is_active=colaborator[0][6],
                manager_id=colaborator[0][7]
            )

            return colab_data
        else:
            raise HTTPException(status_code=401, detail="Login failed")
    else:
        raise HTTPException(status_code=500, detail="Failed to get contributors")