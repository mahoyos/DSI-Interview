from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# Define your data models and schemas here
# For now, using generic examples

# Item model

class ItemPatch(BaseModel):
    """
    Data model for partially updating an existing item.
    
    This model is used when an existing item is being updated with partial data. By providing only the fields 
    that need updating, the model ensures that unnecessary changes are not made to the item in the database.
    """
    name: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(BaseModel):
    """
    Data model for creating a new item.
    
    This model is used when a new item is being created and doesn't have an ID yet. By separating the creation model
    from the general item model, it ensures that the ID is not provided or altered during the creation process.
    """
    name: str
    description: str

class Item(ItemCreate):
    """
    Data model for an existing item.
    
    This model extends the ItemCreate model by including an ID attribute. It's used when an item is being 
    fetched, updated, or deleted. The separation ensures that the ID is always present for existing items,
    making it clear when an item is new (without an ID) versus when it's an existing item (with an ID).
    """
    id: str


# Product Model
    
Base = declarative_base()

class ProductDB(Base):
    """
    Database model representing a product entity.
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)

    def as_dict(self):
        """
        Converts the ProductDB instance into a dictionary.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class ProductPatch(BaseModel):
    """
    Data model for partially updating an existing product.
    
    This model is used when an existing product is being updated with partial data. By providing only the fields 
    that need updating, the model ensures that unnecessary changes are not made to the product in the database.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductCreate(BaseModel):
    """
    Data model for creating a new product.
    
    This model is used when a new product is being created and doesn't have an ID yet. By separating the creation model
    from the general product model, it ensures that the ID is not provided or altered during the creation process.
    """
    name: str
    description: str
    price: float
    
class Product(BaseModel):
    """
    Data model for an existing product.
    
    This model extends the ProductCreate model by including an ID attribute. It's used when a product is being 
    fetched, updated, or deleted. The separation ensures that the ID is always present for existing products,
    making it clear when an product is new (without an ID) versus when it's an existing product (with an ID).
    """
    id: int
    name: str
    description: str
    price: float


# Responser Error Model
class ResponseError(BaseModel):
    """
    Data model for API error responses.
    
    Whenever the API encounters an error, be it a user-made error, a server error, or any other type of error,
    it will respond with this model. Having a standardized error response format ensures that clients can
    easily understand and handle errors consistently. The `detail` attribute provides a descriptive message 
    about the specific error, aiding in debugging and issue resolution.
    """
    detail: str