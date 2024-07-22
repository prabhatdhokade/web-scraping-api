from abc import ABC, abstractmethod
from typing import List
import json
from .models import Product, DBProduct
from .database import SessionLocal


class StorageStrategy(ABC):
    @abstractmethod
    async def save_products(self, products: List[Product]):
        pass


class JSONFileStorage(StorageStrategy):
    async def save_products(self, products: List[Product]):
        with open('products.json', 'w') as f:
            json.dump([product.dict() for product in products], f)


class DatabaseStorage(StorageStrategy):
    async def save_products(self, products: List[Product]):
        db = SessionLocal()
        try:
            for product in products:
                db_product = DBProduct(
                    product_title=product.product_title,
                    product_price=product.product_price,
                    path_to_image=product.path_to_image
                )
                db.add(db_product)
            db.commit()
        finally:
            db.close()
