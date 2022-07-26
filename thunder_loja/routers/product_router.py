from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from thunder_loja.db_handler import DBHandler
from thunder_loja.routers.common_data import ProductData


# Router
router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}},
)


# Logger
logger = logging.getLogger('ProductRoute')


class ProductNewData(BaseModel):
    name: str
    price: float
    description: str
    category: str
    quantity: int


@router.get("/todos")
async def get():
    sql = f"""
           SELECT *
           FROM produto
           ORDER BY prod_id
           """
    db_handler = DBHandler()

    products, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        product_data = []
        
        for product in products:
            product_data.append(
                ProductData(
                    id=product[0],
                    name=product[1],
                    price=product[2],
                    description=product[3],
                    category=product[4],
                    quantity=product[5]
                )
            )
            logger.debug(f"Produto: {product}")
        
        return product_data
    else:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/disponiveis")
async def get():
    sql = f"""
           SELECT *
           FROM produto
           WHERE prod_quant > 0
           ORDER BY prod_id
           """
    db_handler = DBHandler()

    products, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        product_data = []
        
        for product in products:
            product_data.append(
                ProductData(
                    id=product[0],
                    name=product[1],
                    price=product[2],
                    description=product[3],
                    category=product[4],
                    quantity=product[5]
                )
            )
            logger.debug(f"Produto: {product}")
        
        return product_data
    else:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/{id}")
async def get(id: int):
    sql = f"""
           SELECT *
           FROM produto
           WHERE prod_id = {id}
           """
    db_handler = DBHandler()

    product, error_msg = db_handler.send_command(sql)

    if error_msg is None:
        if product:
        
            product_data = ProductData(
                            id=product[0][0],
                            name=product[0][1],
                            price=product[0][2],
                            description=product[0][3],
                            category=product[0][4],
                            quantity=product[0][5])

            logger.debug(f"Produto: {product}")

            return product_data
        
        else:
            logger.debug("Product not found")
            raise HTTPException(status_code=404, detail="Product not found")
        
    else:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/novo")
async def post(product: ProductNewData):
    sql = f"""
           INSERT INTO produto(prod_nome, prod_valor, prod_descricao, prod_categoria, prod_quant)
            VALUES('{product.name}', {product.price}, '{product.description}', '{product.category}', {product.quantity});
           """ 
    
    db_handler = DBHandler()

    _, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    logger.debug("Product added")


@router.put("/atualizar")
async def put(product: ProductData):
    sql = f"""
           UPDATE produto
            SET prod_nome = '{product.name}',
                prod_valor = {product.price},
                prod_descricao = '{product.description}',
                prod_categoria = '{product.category}',
                prod_quant = {product.quantity}
            WHERE prod_id = {product.id}
            RETURNING prod_nome;
           """
    
    db_handler = DBHandler()

    product, error_msg = db_handler.send_command(sql)

    if error_msg is not None:
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

    if not product:
        logger.debug("Product not found")
        raise HTTPException(status_code=404, detail="Product not found")

    logger.debug(f"Product: {product}")