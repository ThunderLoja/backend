from fastapi import APIRouter

router = APIRouter(
    prefix="/venda",
    tags=["venda"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {"message": "Hello Venda"}