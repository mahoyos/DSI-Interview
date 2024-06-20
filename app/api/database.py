from app.api.models.models import ProductDB, ProductCreate, ProductPatch
from app.api.config.db import mysql_db
from typing import List, Optional
from sqlalchemy.orm.exc import NoResultFound

def create_product_in_db(product_data: ProductCreate) -> ProductDB:
    """
    Create a new product in the database.

    Args:
    - product_data (ProductCreate): Data of the product to be created.

    Returns:
    - ProductDB: Created product.

    Raises:
    - Exception: If there's an error during the database operation.
    """
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
    """
    Retrieve all products from the database.

    Returns:
    - List[ProductDB]: List of all products.

    Raises:
    - Exception: If there's an error during the database operation.
    """
    db = mysql_db.SessionLocal()
    try:
        return db.query(ProductDB).all()
    except Exception as e:
        raise e

def get_product_by_id(product_id: int) -> Optional[ProductDB]:
    """
    Retrieve a product from the database by its ID.

    Args:
    - product_id (int): ID of the product to be fetched.

    Returns:
    - Optional[ProductDB]: Fetched product if found, else None.

    Raises:
    - Exception: If there's an error during the database operation.
    """
    db = mysql_db.SessionLocal()
    try:
        return db.query(ProductDB).filter(ProductDB.id == product_id).first()
    except Exception as e:
        raise e

def delete_product_by_id(product_id: int) -> ProductDB:
    """
    Delete a product from the database by its ID.

    Args:
    - product_id (int): ID of the product to be deleted.

    Returns:
    - ProductDB: Deleted product if found and deleted successfully.

    Raises:
    - NoResultFound: If no product is found with the given ID.
    - Exception: If there's an error during the database operation.
    """
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
    """
    Update a product in the database.

    Args:
    - product_id (int): ID of the product to be updated.
    - product_update (ProductPatch): Data with which the product is to be updated.

    Returns:
    - Optional[ProductDB]: Updated product if found and updated successfully, else None.

    Raises:
    - Exception: If there's an error during the database operation.
    """
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
