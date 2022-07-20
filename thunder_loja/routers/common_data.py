import datetime
from pydantic import BaseModel


class ColabData(BaseModel):
    id: int
    name: str
    cpf: int
    salary: float
    admission_date: datetime.date
    colab_type: int
    is_active: bool
    manager_id: int = None
    password: str


class ProductData(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    quantity: int
