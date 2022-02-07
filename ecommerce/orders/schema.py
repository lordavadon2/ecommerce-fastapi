import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, EmailStr

from ecommerce.products.schema import ProductListing


class ShowOrderDetails(BaseModel):
    id: int
    order_id: int
    product_order_details: ProductListing

    class Config:
        orm_mode = True


class ShowOrder(BaseModel):
    id: Optional[int]
    order_date: datetime.datetime
    order_amount: float
    order_status: str
    shipping_address: str
    order_details: List[ShowOrderDetails] = []

    class Config:
        orm_mode = True
