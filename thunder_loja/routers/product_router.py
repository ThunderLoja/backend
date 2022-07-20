from fastapi import APIRouter
from pydantic import BaseModel


# Data
class ProductData(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str


# Router
router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}")
async def get(id: int):
    return {"message": f"Hello Produto {id}"}


@router.post("/")
async def post(product: ProductData):
    return {"message": f"Hello Produto {product.name}"}


@router.put("/")
async def put(product: ProductData):
    return {"message": f"Hello Produto {product.name}"}