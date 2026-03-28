from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    amount: float
    description: str | None = None


class TransactionCreate(TransactionBase):
    user_id: int
    category_id: int


class TransactionUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    user_id: int | None = None
    category_id: int | None = None


class TransactionResponse(TransactionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
