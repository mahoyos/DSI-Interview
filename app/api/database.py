from app.api.models.models import ProductDB, ProductCreate
from app.api.config.db import mysql_db

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
