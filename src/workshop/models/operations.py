from pydantic import BaseModel

from datetime import date
from typing import Optional
from enum import Enum
from decimal import Decimal


class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class Operation(BaseModel):
    id: int
    date: date
    operation: OperationKind
    amount: Decimal
    description: Optional[str]

    class Config:
        orm_mode = True
