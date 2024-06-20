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
|   |   |
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
└── requirements.txt \


## Configuration Instructions

1. **Environment Setup**: Ensure you have Python 3.8 or higher installed.
2. **Install Dependencies**: Run 'pip install -r requirements.txt' to install the necessary dependencies.
3. **Environment Variables**: Configure the required environment variables as described in 'app/api/config/env.py'.
4. **Run tests**: Execute 'PYTHONPATH=./ pytest' to start running the tests.  (The warnings related to the deprecated use of async came from the initial repository and were not addressed, as it was not the project's objective to correct them).
5. **Run the Server**: Execute 'uvicorn app.app:app --reload --port 8000' to start the development server on port 8000.

## Endpoints

The project provides a series of endpoints to perform CRUD operations on `items` and `products`. The endpoints for Items are disabled because the credentials were not available and the project's focus was on products (which are functioning without any issues):

- `POST /items/`: Creates a new product.
- `GET /items/`: Lists all products.
- `GET /items/{item_id}/`: Retrieves a specific product by ID.
- `PUT /items/{item_id}/`: Updates a product by ID.
- `PATCH /items/{item_id}/`: Partial update of an item by ID.
- `DELETE /items/{item_id}/`:  Deletes a specific product by ID.

- `POST /items/`: Creates a new product.
- `GET /items/`: Lists all products.
- `GET /items/{item_id}/`: Retrieves a specific product by ID.
- `PATCH /items/{item_id}/`: Updates a product by ID.
- `DELETE /items/{item_id}/`:  Deletes a specific product by ID.

## Contributions

If you wish to contribute to the project, please follow these guidelines:

1. **Fork the repository**: Fork the repository and clone your fork to your local machine.

2. **Create a new branch**: Create a branch with a descriptive name based on the functionality or fix you are implementing.
3. **Make your changes**: Make and test your changes in that branch.
4. **Submit a pull request**: Once you are finished, submit a pull request to the original repository.

## License

This project is under an open-source license.