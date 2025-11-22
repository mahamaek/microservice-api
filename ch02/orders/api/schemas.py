from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, conlist, conint, field_validator

class Size(Enum):
    small = 'small'
    medium = 'medium'
    big = 'big'

class Status(Enum):
    created = 'created'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Annotated[int, Field(strict=True, ge=1)] = 1

    @field_validator('quantity')
    def quantity_non_nullable(cls, value):
        if value is None:
            raise ValueError('quantity may not be None')
        return value
    
class CreateOrderSchema(BaseModel):
    order: Annotated[List[OrderItemSchema], Field(min_items=1)]


class GetOrdersSchema(BaseModel):
    id: UUID
    created: datetime
    status: Status