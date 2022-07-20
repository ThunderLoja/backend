import logging
import datetime
from typing import List
import psycopg2
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


class ItenData(BaseModel):
    product_id: int
    quantity_sold: int


class SaleData(BaseModel):
    id: int
    value: float
    date: datetime.date
    description: str
    client_cpf: int
    seller_id: int
    itens: List[ItenData] = []


class NewSaleData(BaseModel):
    value: float
    date: datetime.date
    description: str
    client_cpf: int
    seller_id: int
    itens: List[ItenData]


# Router
router = APIRouter(
    prefix="/venda",
    tags=["venda"],
    responses={404: {"description": "Not found"}},
)


# Logger
logger = logging.getLogger('SaleRoute')

@router.get("/todas")
async def get():
    sql = f"""
        SELECT tr_id, tr_valor, tr_data, tr_descricao, clt_cpf, colab_id
        FROM transacao
        NATURAL JOIN venda
        """
    db_handler = DBHandler()

    sales, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        client_data = []
        
        for sale in sales:
            
            data = SaleData(
                id=sale[0],
                value=sale[1],
                date=sale[2],
                description=sale[3],
                client_cpf=sale[4],
                seller_id=sale[5],
            )

            sql = f"""
                SELECT *
                FROM prod_venda
                WHERE tr_id = {data.id}
                """

            sale_itens, _ = db_handler.send_command(sql)

            for iten in sale_itens:
                iten_data = ItenData(
                    product_id=iten[1],
                    quantity_sold=iten[2]
                )
            
                data.itens.append(iten_data)

            client_data.append(data)
            logger.debug(f"Sale: {sale}")
        
        return client_data
    else:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

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
async def post(sale_data: NewSaleData):
    db_handler = DBHandler()

    logger.debug(f"Sale data: {sale_data}")

    error_msg = None
    status_code = 200

    try:
        conn = db_handler.connect()
        cur = conn.cursor()

        # Criar nova linha em transacao
        sql = f"""
            INSERT INTO transacao(tr_valor, tr_data, tr_descricao, tr_tipo)
            VALUES({sale_data.value}, '{sale_data.date}', '{sale_data.description}', 2) RETURNING tr_id;
            """

        cur.execute(sql)
        tr_id = cur.fetchone()[0]

        logger.debug(f"New sales id: {tr_id}")

        # Criar nova linha em venda
        sql = f"""
            INSERT INTO venda(tr_id, clt_cpf, colab_id)
            VALUES({tr_id}, {sale_data.client_cpf}, {sale_data.seller_id});
            """

        cur.execute(sql)

        # Iterar pelo array, subtraindo a quantidade do produto e adicionando cada linha a prod_venda
        for iten in sale_data.itens:
            sql = f"""
                SELECT prod_quant
                FROM produto
                WHERE prod_id = {iten.product_id}
                """
            cur.execute(sql)
            prod_quant = cur.fetchone()[0]

            if prod_quant < iten.quantity_sold:
                raise ValueError("Not enough products to make this sell")
            
            sql = f"""
                UPDATE produto
                SET prod_quant = prod_quant - {iten.quantity_sold}
                WHERE prod_id = {iten.product_id}
                """
            cur.execute(sql)

            sql = f"""
                INSERT INTO prod_venda(tr_id, prod_id, vend_quant)
                VALUES({tr_id}, {iten.product_id}, {iten.quantity_sold});
                """
            cur.execute(sql)

        conn.commit()
        cur.close()
    except ValueError as error:
        logger.error(error)
        error_msg = str(error)
        status_code = 400
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        error_msg = str(error)
        status_code = 500
    finally:
        db_handler.disconnect()

    if error_msg is not None:
        raise HTTPException(status_code=status_code, detail=error_msg)
    
