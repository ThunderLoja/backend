import logging
from fastapi import FastAPI

from thunder_loja.routers import client_router, login_router, product_router, sale_router, seller_router
from thunder_loja.db_handler import DBHandler

# Config logger
logging.basicConfig(level=logging.INFO)

# Create singleton to handle DB connection
db_handler = DBHandler()
db_handler.initialise(config_file="cfg/database.ini",
                      config_section="thunder_loja_db")

# Create app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello ThunderLoja"}

app.include_router(client_router.router)
app.include_router(login_router.router)
app.include_router(product_router.router)
app.include_router(sale_router.router)
app.include_router(seller_router.router)