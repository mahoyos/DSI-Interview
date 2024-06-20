# DSI Interview

This project aimed to create a straightforward CRUD (Create, Read, Update, Delete) API in FastAPI for managing products. It follows a standard API structure and enables users to perform basic operations like creating, reading, updating, and deleting product information in a relational database. MySQL was chosen as the backend database. The coding standards from the initially provided repository were followed as much as possible, but certain decisions were made as deemed appropriate.

## Project structure
.
├── app \
│   ├── api \
│   │   ├── adapters \
│   │   │   └── README.md # Adapters explanation for external services. \
│   │   ├── auth \
│   │   │   ├── auth.py # Authentication related operations. \
│   │   ├── config \
│   │   │   ├── db.py # Database configuration. \
│   │   │   ├── env.py # Environment variables. \
│   │   │   ├── exceptions.py # Project-specific exceptions. \
│   │   ├── database.py #Functions and operations with DB \
│   │   ├── methods \
│   │   │   ├── methods.py \
│   │   │   └── README.md # Utility functions explanation for routes. \
│   │   ├── models \
│   │   │   ├── models.py # Pydantic and sqlalchemy models. \
│   │   ├── routes \
│   │   │   ├── README.md \
│   │   │   └── routes.py # API routes. \
│   │   └── test \
│   │       └── test_endpoints.py \
│   ├── app.py # Entry point for the FastAPI application. \
├── Dockerfile \
├── README.md \
└── requirements.txt 

## Database configuration

For this project, MySQL was chosen as the relational database. It is hosted locally, and proper configuration is essential for the project to function correctly.

The "interview" database consists solely of a "products" table. This table has four columns defined in the model as follows:

**id**: Column(Integer, primary_key=True, index=True, autoincrement=True)
**name**: Column(String, index=True)
**description**: Column(String, index=True)
**price**: Column(Float)

To set up the required database for this project, follow these steps:

1. **Log in to MySQL**:
    ```bash
    mysql -u root -p
    ```

2. **Create the "interview" database**:
    ```sql
    CREATE DATABASE interview;
    ```

3. **Create a user and grant privileges for the database**:
    ```sql
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'root';
    GRANT ALL PRIVILEGES ON interview.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    ```

4. **Select the "interview" database**:
    ```sql
    USE interview;
    ```

5. **Create the "products" table**:
    ```sql
    CREATE TABLE products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL
    );
    ```

With these steps, the required database for the project will be set up and ready for use.

## Configuration Instructions

0. **Clone the repository** Run `git clone https://github.com/mahoyos/DSI-Interview`
1. **Environment Setup**: Ensure you have Python 3.8 or higher installed.
2. **Install Dependencies**: Go to the directory where you cloned the project and Run `pip install -r requirements.txt` to install the necessary dependencies.
3. **Create Database**: Create the database as explained in the Database Configuration section.
4. **Environment Variables**: Configure the required environment variables as described in `app/api/config/env.py` as you need. (The .env file should never be uploaded to a repository. However, for practicality and ease of execution, an exception was made in this case. If you are not going to make changes, proceed to the next step. )
5. **Run tests**: Execute `PYTHONPATH=./ pytest` to start running the tests.  (The warnings related to the deprecated use of async came from the initial repository and were not addressed, as it was not the project's objective to correct them.)
6. **Run the Server**: Execute `uvicorn app.app:app --reload --port 8000` to start the development server on port 8000.


## Endpoints

The project provides a series of endpoints to perform CRUD operations on `items` and `products`. The endpoints for Items are disabled because the credentials were not available and the project's focus was on products (which are functioning without any issues):

### Items

- `POST /items/`: Creates a new product.
- `GET /items/`: Lists all products.
- `GET /items/{item_id}/`: Retrieves a specific product by ID.
- `PUT /items/{item_id}/`: Updates a product by ID.
- `PATCH /items/{item_id}/`: Partial update of an item by ID.
- `DELETE /items/{item_id}/`:  Deletes a specific product by ID.

### Products

- `POST /items/`: Creates a new product.
- `GET /items/`: Lists all products.
- `GET /items/{item_id}/`: Retrieves a specific product by ID.
- `PATCH /items/{item_id}/`: Updates a product by ID.
- `DELETE /items/{item_id}/`:  Deletes a specific product by ID.

### Curl Commands for Testing Endpoints
Below are the curl commands that use curl to facilitate the process of testing the endpoints. Replace {product_id} for the ID of a product.

- CREATE_PRODUCT_CURL=`curl -X POST http://localhost:8000/api/v1/example/products/ -H "Content-Type: application/json" -d "{\"name\": \"Name\", \"description\": \"Description\", \"price\": 19.99}"`

- GET_ALL_PRODUCTS_CURL=`curl -X GET "http://localhost:8000/api/v1/example/products/" -H "Content-Type: application/json"`

- GET_PRODUCT_BY_ID_CURL=`curl -X GET "http://localhost:8000/api/v1/example/products/{product_id}/" -H "Content-Type: application/json"`

- DELETE_PRODUCT_BY_ID_CURL=`curl -X DELETE http://localhost:8000/api/v1/example/products/{product_id}/`

- UPDATE_PRODUCT_BY_ID_CURL=`curl -X PATCH "http://localhost:8000/api/v1/example/products/{product_id}/" -H "Content-Type: application/json" -d "{\"name\": \"New_name\", \"description\": \"New_Description\", \"price\": 99.99}"`

## Contributions

If you wish to contribute to the project, please follow these guidelines:

1. **Fork the repository**: Fork the repository and clone your fork to your local machine.

2. **Create a new branch**: Create a branch with a descriptive name based on the functionality or fix you are implementing.
3. **Make your changes**: Make and test your changes in that branch.
4. **Submit a pull request**: Once you are finished, submit a pull request to the original repository.

## License

This project is under an open-source license.