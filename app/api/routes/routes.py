from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
#from bson import ObjectId
#import pymongo.errors
from typing import List
import logging

# Configuration, models, methods and authentication modules imports

#from app.api.config.db import database
from app.api.config.limiter import limiter
from app.api.config.env import API_NAME
from app.api.models.models import ResponseError, ItemPatch, ItemCreate, Item, Product, ProductCreate, ProductPatch
from app.api.auth.auth import auth_handler
#from app.api.methods.methods import is_valid_objectid, convert_objectid_to_str, handle_error
from app.api.database import create_product_in_db, get_all_products, get_product_by_id, delete_product_by_id, update_product_in_db

router = APIRouter()

# Log file name
log_filename = f"api_{API_NAME}.log"

# Configurate the logging level to catch all messages from DEBUG onwards
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    handlers=[logging.FileHandler(log_filename),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)


# Products routes

@router.post('/products/',
             response_model=Product,
             status_code=status.HTTP_201_CREATED,
             tags=["CRUD"],
             responses={
                 500: {"model": ResponseError, "description": "Internal server error."},
                 429: {"model": ResponseError, "description": "Too many requests."}
             }
             )
@limiter.limit("5/minute")
def create_product(product: ProductCreate, request: Request):
    """
    Create a new product in the database.

    Args:
        - product (ProductCreate): Product to be created.

    Returns:
        - Product: Created product with its ID.

    Raises:
        - HTTPException: If the product creation fails or if there are too many requests.
    """
    try:
        new_product = create_product_in_db(product)
        
        if not new_product:
            raise HTTPException(status_code=500, detail="Product creation failed.")
        
        product = new_product.as_dict()
        return product
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get('/products/', 
            response_model=List[Product], 
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Not items found."},
            })
@limiter.limit("5/minute")
def get_products(request: Request):
    """
    Retrieve all products from the database.

    Returns:
        - List[Product]: List of products.

    Raises:
        - HTTPException: If there is an error retrieving products or if there are too many requests.
    """
    try:
        products = [product.as_dict() for product in get_all_products()]
        return products
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        logger.error(f"Error retrieving products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get('/products/{product_id}/', 
            response_model=Product, 
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Product not found"},
            })
@limiter.limit("5/minute")
def get_product(product_id: int, request: Request):
    """
    Retrieve a product by its ID from the database.

    Args:
        - product_id (int): ID of the product to retrieve.

    Returns:
        - Product: Retrieved product.

    Raises:
        - HTTPException: If the product is not found or if there are too many requests.
    """
    try:
        product = get_product_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product.as_dict()
    except HTTPException as http_exception:
        raise http_exception
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        logger.error(f"Error retrieving product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    
@router.delete('/products/{product_id}/',
               response_model=Product,
               tags=["CRUD"],
               responses={
                   500: {"model": ResponseError, "description": "Internal server error."},
                   429: {"model": ResponseError, "description": "Too many requests."},
                   404: {"model": ResponseError, "description": "Product not found or not deleted."},
               })
@limiter.limit("5/minute")
def delete_product(product_id: int, request: Request):
    """
    Delete a product by its ID from the database.

    Args:
        - product_id (int): ID of the product to delete.

    Returns:
        - Product: Deleted product.

    Raises:
        - HTTPException: If the product is not found, not deleted, or if there are too many requests.
    """
    try:
        product_deleted = delete_product_by_id(product_id)
        print("Product deleted es" + str(product_deleted) + str(type(product_deleted)))
        if product_deleted is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_deleted.as_dict()
    except HTTPException as http_exception:
        raise http_exception
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
    
@router.patch('/products/{product_id}/',
              response_model=Product,
              tags=["CRUD"],
              responses={
                  500: {"model": ResponseError, "description": "Internal server error."},
                  429: {"model": ResponseError, "description": "Too many requests."},
                  404: {"model": ResponseError, "description": "Product not found or not updated."},
              })
@limiter.limit("5/minute")
def update_product(product_id: int, product_update: ProductPatch, request: Request):
    """
    Update a product by its ID in the database.

    Args:
        - product_id (int): ID of the product to update.
        - product_update (ProductPatch): Updated product data.

    Returns:
        - Product: Updated product.

     Raises:
        - HTTPException: If the product is not found, not updated, or if there are too many requests.
    """
    try:
        product = get_product_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        updated_product = update_product_in_db(product_id, product_update)

        if updated_product is None:
            raise HTTPException(status_code=500, detail="Product update failed.")

        return updated_product.as_dict()
    except HTTPException as http_exception:
        raise http_exception
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
'''
These endpoints are commented out because there is no connection to MongoDB, 
which causes errors. When the connection with MongoDB is available, they can 
be uncommented.

# Item routes
    
@router.post('/items/', 
             response_model=Item, 
             status_code=status.HTTP_201_CREATED, 
             tags=["CRUD"],
             responses={
                 500: {"model": ResponseError, "description": "Internal server error."},
                 429: {"model": ResponseError, "description": "Too many requests."}
             })
@limiter.limit("5/minute")
def create_item(item: ItemCreate, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Create a new item in the database.
    
    Args:
    - item (ItemCreate): Item to be created.
    
    Returns:
    - Item: Created item with its ID.
    """
    try:
        logger.info("Creating a new item.")
        new_item = database.items.insert_one(item.dict())
        if not new_item.inserted_id:
            logger.warning("Failed to create a new item.")
            raise HTTPException(status_code=500, detail="Item creation failed.")
        logger.info(f"Item with ID {str(new_item.inserted_id)} successfully created.")
        item = item.dict()
        item["id"] = str(new_item.inserted_id)
        return item
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

@router.get('/items/', 
            response_model=List[Item],
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Not items found."},
            })
@limiter.limit("5/minute")
def list_items(request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Fetch all items from the database.
    
    Returns:
    - List[Item]: List of items.
    """
    try:
        logger.info("Fetching all items.")
        items = list(database.items.find())
        if not items:
            logger.warning("No items found in the database.")
            raise HTTPException(status_code=404, detail="No items found.")
        logger.info("Items successfully fetched.")
        items = convert_objectid_to_str(items)
        return items
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

@router.get('/items/{item_id}/',
            response_model=Item,
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Item not found."},
                400: {"model": ResponseError, "description": "Invalid item_id format."},
            })
@limiter.limit("5/minute")
def get_item(item_id: str, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Fetch a single item from the database using its ID.
    
    Args:
    - item_id (str): ID of the item to be fetched.
    
    Returns:
    - Item: Fetched item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Fetching item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        item = database.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            logger.warning(f"No item found with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found.")
        logger.info(f"Item with ID {item_id} successfully fetched.")
        item = convert_objectid_to_str(item)
        return item
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

@router.put('/items/{item_id}/', 
            response_model=Item,
            tags=["CRUD"],
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."},
                404: {"model": ResponseError, "description": "Item not found or not updated."},
                400: {"model": ResponseError, "description": "Invalid item_id format."},
            })
@limiter.limit("5/minute")
def update_item(item_id: str, item_update: ItemCreate, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Updating item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        updated_item = database.items.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": item_update.dict()}, return_document=True)
        if not updated_item:
            logger.warning(f"Failed to update item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not updated.")
        logger.info(f"Item with ID {item_id} successfully updated.")
        updated_item = convert_objectid_to_str(updated_item)
        return updated_item
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

@router.patch('/items/{item_id}/',
              response_model=Item,
              tags=["CRUD"],
              responses={
                  500: {"model": ResponseError, "description": "Internal server error."},
                  429: {"model": ResponseError, "description": "Too many requests."},
                  404: {"model": ResponseError, "description": "Item not found or not patched."},
                  400: {"model": ResponseError, "description": "Invalid item_id format."},
              })
@limiter.limit("5/minute")
def patch_item(item_id: str, item_patch: ItemPatch, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Partially update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Partially updating item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        updated_item = database.items.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": item_patch.dict()}, return_document=True)
        if not updated_item:
            logger.warning(f"Failed to patch item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not patched.")
        logger.info(f"Item with ID {item_id} successfully patched.")
        updated_item = convert_objectid_to_str(updated_item)
        return updated_item
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

@router.delete('/items/{item_id}/',
               response_model=Item,
               tags=["CRUD"],
               responses={
                   500: {"model": ResponseError, "description": "Internal server error."},
                   429: {"model": ResponseError, "description": "Too many requests."},
                   404: {"model": ResponseError, "description": "Item not found or not deleted."},
                   400: {"model": ResponseError, "description": "Invalid item_id format."},
               })
@limiter.limit("5/minute")
def delete_item(item_id: str, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Delete an item from the database.
    
    Args:
    - item_id (str): ID of the item to be deleted.
    
    Returns:
    - Item: Deleted item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        logger.info(f"Deleting item with ID {item_id}.")
        if not is_valid_objectid(item_id):
            raise HTTPException(status_code=400, detail="Invalid item_id format.")
        deleted_item = database.items.find_one_and_delete({"_id": ObjectId(item_id)})
        if not deleted_item:
            logger.warning(f"Failed to delete item with ID {item_id}.")
            raise HTTPException(status_code=404, detail="Item not found or not deleted.")
        logger.info(f"Item with ID {item_id} successfully deleted.")
        deleted_item = convert_objectid_to_str(deleted_item)
        return deleted_item
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

"""
This module serves as an example of using FastAPI's BackgroundTasks feature.

BackgroundTasks allow you to run functions in the background of a request. This is particularly useful when you want to execute time-consuming tasks without making the client wait for the result. The task runs in the same process (no new processes are spawned) but is executed after the response has been sent to the client. 

Advantages:
1. Improved Response Times: By delegating lengthy tasks to the background, you can return responses to clients more swiftly.
2. Resource Optimization: Offloading non-critical tasks to run post-response means the main thread remains unblocked, and can process other incoming requests.
3. Better User Experience: Especially for web applications, users do not need to wait for long operations to complete, ensuring smoother interactions.

Using BackgroundTasks is essential when you want to ensure that the user isn't kept waiting, while still completing all necessary operations. It's a balance between responsiveness and completeness.

Note: Although the task is running in the background, if the main process stops (e.g., the server crashes or is stopped), the background tasks will also be terminated. It's important to ensure that these tasks are resilient and can handle such interruptions.
"""

from fastapi import BackgroundTasks
import time

def simulate_email_sending(email: str):
    """Simulate email sending delay."""
    time.sleep(5)
    print(f"Email sent to {email}")

@router.post('/send-email/',
             tags=["Background Tasks"],
             responses={
                 500: {"model": ResponseError, "description": "Internal server error."},
                 429: {"model": ResponseError, "description": "Too many requests."}
             })
@limiter.limit("5/minute")
def send_email_background(email: str, background_tasks: BackgroundTasks, request: Request):#, auth=Depends(auth_handler.authenticate)):
    """Endpoint to send an email in the background.
    
    Args:
    - email (str): Email address to which the email will be sent.
    
    Returns:
    - dict: Confirmation message.
    """
    try:
        logger.info(f"Queuing email for {email}.")
        background_tasks.add_task(simulate_email_sending, email)
        logger.info(f"Email for {email} has been queued successfully.")
        return {"message": "Email is being sent in the background"} # Example response body
    except pymongo.errors.PyMongoError as e:
        # Handle any PyMongo errors here
        logger.critical(f"Error interacting with the database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating password.")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e, logger)

'''