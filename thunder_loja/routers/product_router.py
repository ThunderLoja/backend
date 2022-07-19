from fastapi import APIRouter

router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {"message": "Hello Produto"}