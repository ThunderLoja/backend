import logging
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from thunder_loja.db_handler import DBHandler


# Data
class SaleReportData(BaseModel):
    id: int
    name: str
    price: float
    quantity_available: int
    quantity_sold: int

# Router
router = APIRouter(
    prefix="/venda",
    tags=["venda"],
    responses={404: {"description": "Not found"}},
)


# Logger
logger = logging.getLogger('SaleRoute')


@router.get("/relatorio")
async def get(start: datetime.date = None, end: datetime.date = None):
    # Join 
    logger.debug(f"Parameters: {start} {end}")

    where_string = ""
    if start is not None:
        if end is not None:
            if start > end:
                raise HTTPException(status_code=400, detail='Start date greater then end date')
            where_string = f"WHERE tr_data between '{start}' and '{end}'"
        
        else:
            where_string = f"WHERE tr_data >= '{start}'"
    else:
        if end is not None:
            where_string = f"WHERE tr_data <= '{end}'"

    sql = f"""
           SELECT prod_id, prod_nome, prod_valor, prod_quant, sum(vend_quant)
           FROM produto
           NATURAL JOIN prod_venda
           NATURAL JOIN transacao
           {where_string}
           GROUP BY prod_id, prod_nome, prod_valor, prod_quant
           ORDER BY prod_id
           """
    db_handler = DBHandler()

    products, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        report_data = []
        
        for product in products:
            report_data.append(
                SaleReportData(
                    id=product[0],
                    name=product[1],
                    price=product[2],
                    quantity_available=product[3],
                    quantity_sold=product[4]
                )
            )
            logger.debug(f"Product report: {product}")
        
        return report_data
    else:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/nova")
async def post(sale_data: SaleReportData):
    # Dados do json: transação, venda, [(prod_id, quant)...]
    # Criar nova linha em transacao
    # Criar nova linha em venda
    # Iterar pelo array, subtraindo a quantidade do produto e adicionando cada linha a prod_venda
    # Commit
    return {"message": f"Hello Venda {sale_data.transaction_id}"}
