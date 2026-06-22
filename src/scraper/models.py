from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime


class Product(BaseModel):

    product_id: str
    handle: Optional[str] = None
    name: str
    price: float = Field(gt=0)
    category: Optional[str] = None
    availability: bool = True
    source_url: Optional[str] = None
    sku: Optional[str] = None
    scraped_at: datetime


