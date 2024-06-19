from app.api.models.models import ProductDB, ProductCreate
from app.api.config.db import mysql_db
from typing import List, Optional

def create_product_in_db(product_data: ProductCreate) -> ProductDB:

    db = mysql_db.SessionLocal()
    try:
        new_product = ProductDB(name=product_data.name, description=product_data.description, price=product_data.price)

        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    
    except Exception as e:
        db.rollback()
        raise e

def get_all_products() -> List[ProductDB]:
    db = mysql_db.SessionLocal()
    try:
        return db.query(ProductDB).all()
    except Exception as e:
        raise e
    
def get_product_by_id(product_id: int) -> Optional[ProductDB]:
    db = mysql_db.SessionLocal()
    try:
        return db.query(ProductDB).filter(ProductDB.id == product_id).first()
    except Exception as e:
        raise e