from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, String, Float
from .database import Base


class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_title = Column(String, index=True)
    product_price = Column(String)
    path_to_image = Column(String)


class ScrapingSettings(BaseModel):
    target_url: str
    page_limit: Optional[int] = None
    proxy: Optional[str] = None


class Product(BaseModel):
    product_title: str
    product_price: str
    path_to_image: str
