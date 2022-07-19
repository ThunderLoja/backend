from fastapi import APIRouter

router = APIRouter(
    prefix="/vendedor",
    tags=["vendedor"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {"message": "Hello Vendedor"}