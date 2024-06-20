from app.api.models.models import ProductDB, ProductCreate, ProductPatch
from app.api.config.db import mysql_db
from typing import List, Optional
from sqlalchemy.orm.exc import NoResultFound


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
    
def delete_product_by_id(product_id: int) -> ProductDB:
    db = mysql_db.SessionLocal()
    try:
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if product is None:
            return None
        db.delete(product)
        db.commit()
        return product
    except NoResultFound:
        return None
    except Exception as e:
        raise e
    
def update_product_in_db(product_id: int, product_update: ProductPatch) -> Optional[ProductDB]:
    db = mysql_db.SessionLocal()
    try:
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
        if not product:
            return None

        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise e