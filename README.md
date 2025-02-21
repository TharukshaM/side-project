# Furniture Store API

## Description

The Furniture Store API is a RESTful API built with Django and Django REST Framework. It provides endpoints for managing a furniture store, including user authentication, furniture inventory management, shopping cart functionality, and order processing. The API is designed to be used by front-end applications or other services that need to interact with a furniture store's backend.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (optional, SQLite is used by default)
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/furniture-store-api.git
   cd furniture-store-api
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:

   By default, the project uses SQLite. If you want to use PostgreSQL, update the `DATABASES` setting in `furniture_store/settings.py` with your PostgreSQL credentials.
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`.

### Endpoints

#### Authentication

- **Register a new user**
  - **POST** `/auth/register/`
  - Request Body:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "address": "string"
    }
    ```

- **User login**
  - **POST** `/auth/login/`
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

- **Get user profile**
  - **GET** `/auth/profile/`
  - Requires authentication.

#### Furniture

- **List all furniture items**
  - **GET** `/furniture/`

- **Create a new furniture item**
  - **POST** `/furniture/`
  - Request Body:
    ```json
    {
      "name": "string",
      "description": "string",
      "category": "string",
      "price": "number",
      "dimensions": "string"
    }
    ```
#### Inventory

- **Create a new Inventory Entry**
  - **POST** `/inventory/`
  - Request Body:
    ```json
    {
      "furniture": "integer",
      "quantity": "integer"
    }
    ```

#### Shopping Cart

- **View shopping cart**
  - **GET** `/shopping-cart/`
  - Requires authentication.

- **Add item to shopping cart**
  - **POST** `/shopping-cart/`
  - Request Body:
    ```json
    {
      "furniture_id": "integer",
      "quantity": "integer"
    }
    ```

#### Checkout

- **Checkout and place an order**
  - **POST** `/checkout/checkout/`
  - Request Body:
    ```json
    {
      "payment_method": "string",
      "address": "string"
    }
    ```

#### Orders

- **Get user orders**
  - **GET** `/order/`
  - Requires authentication.

- **Get order details**
  - **GET** `/order/{order_id}/`
  - Requires authentication.

- **Update order status (Admin only)**
  - **POST** `/order/{order_id}/update_status/`
  - Request Body:
    ```json
    {
      "status": "string"
    }
    ```

### Authentication

The API uses token-based authentication. After logging in, you will receive a token that you need to include in the `Authorization` header for authenticated requests:

```http
Authorization: Token <your_token_here>
```

## Running Tests

To run the tests, use the following command:
```bash
pytest api/tests/
```
## CI/CD

The project includes a GitHub Actions workflow (`ci-pipeline.yml`) that runs linting and tests on every push to the `main` branch or when a pull request is opened.
