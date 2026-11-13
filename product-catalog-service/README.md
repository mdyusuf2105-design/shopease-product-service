# ShopEase – Product Catalog Microservice

## 1. Project Overview

The ShopEase Product Catalog Service is an independent microservice developed using FastAPI and MySQL.

It manages product information, product categories, and inventory transactions. It communicates with the authentication service through JWT-based authentication.

This service is maintained separately from the existing ShopEase Product Service.

## 2. Technology Stack

- Python 3.11
- FastAPI
- MySQL 8.0
- SQLAlchemy ORM
- Alembic
- Pydantic
- JWT Authentication
- Docker
- Docker Compose
- Uvicorn

## 3. Architecture

The service follows a layered architecture:

- Routers: Handle HTTP requests and responses.
- Schemas: Validate incoming and outgoing data.
- Services: Contain business logic.
- Models: Define database tables and relationships.
- Database: Manage MySQL connections and sessions.
- Core: Manage application settings and JWT authentication.

## 4. Database Design

The service uses a separate MySQL database:

`shopease_product_catalog_db`

### Categories

Stores product category information.

Fields:
- id
- name
- description
- is_active
- created_at
- updated_at

### Products

Stores product details.

Fields:
- id
- category_id
- name
- description
- sku
- price
- discount_price
- stock_quantity
- image_url
- brand
- is_active
- created_at
- updated_at

### Inventory Transactions

Maintains stock movement history.

Fields:
- id
- product_id
- transaction_type
- quantity
- previous_stock
- updated_stock
- remarks
- created_at

## 5. API Endpoints

Base URL:

`http://localhost:8005`

### Product APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/products/ | Create product |
| GET | /api/products/ | List and search products |
| GET | /api/products/{product_id} | Get product details |
| PUT | /api/products/{product_id} | Replace product details |
| PATCH | /api/products/{product_id} | Partially update product |
| DELETE | /api/products/{product_id} | Deactivate product |

Product listing supports:
- Search by product name or SKU
- Category filtering
- Minimum and maximum price
- Availability filtering
- Pagination
- Sorting

### Category APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/categories/ | Create category |
| GET | /api/categories/ | List categories |
| GET | /api/categories/{category_id} | Get category details |
| PUT | /api/categories/{category_id} | Replace category details |
| PATCH | /api/categories/{category_id} | Partially update category |
| DELETE | /api/categories/{category_id} | Delete category |

### Inventory APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/inventory/{product_id} | Get current inventory |
| POST | /api/inventory/stock-in/{product_id} | Add stock |
| POST | /api/inventory/stock-out/{product_id} | Remove stock |
| GET | /api/inventory/{product_id}/history | View stock history |
| GET | /api/inventory/low-stock | View low-stock products |

## 6. Authentication and Authorization

The service validates JWT access tokens using the shared authentication secret.

Authorization rules:

### Admin
- Create, update, and deactivate products.
- Create, update, and delete categories.
- Manage inventory.
- View inventory history and low-stock products.

### Customer
- View active products.
- Search and filter active products.
- View active categories.

### HTTP Status Codes

- 200 – Successful request
- 201 – Resource created
- 401 – Missing or invalid authentication token
- 403 – Insufficient permissions
- 404 – Resource not found
- 409 – Resource conflict
- 422 – Validation error

## 7. Environment Configuration

Create your local environment file:

`cp .env.example .env`

Configure the following variables:

- APP_NAME
- APP_VERSION
- APP_PORT
- MYSQL_ROOT_PASSWORD
- MYSQL_DATABASE
- MYSQL_USER
- MYSQL_PASSWORD
- DATABASE_URL
- JWT_SECRET_KEY
- JWT_ALGORITHM
- LOW_STOCK_THRESHOLD

The JWT secret must match the secret used by the authentication service.

Never commit `.env` or publish actual secrets.

## 8. Running with Docker

From the product-catalog-service directory:

```bash
docker compose up --build -d
```

The Docker Compose configuration starts:
- MySQL 8.0
- Product Catalog FastAPI service

MySQL uses a persistent Docker volume.

The application runs database migrations through Alembic before starting Uvicorn.

Service URL:

`http://localhost:8005`

API documentation:

`http://localhost:8005/docs`

## 9. Database Migrations

Alembic manages database schema migrations.

Migration commands:

```bash
alembic revision --autogenerate -m "migration description"
```

```bash
alembic upgrade head
```

```bash
alembic downgrade -1
```

## 10. Project Structure

```text
product-catalog-service/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── category_model.py
│   │   ├── product_model.py
│   │   └── inventory_model.py
│   │
│   ├── schemas/
│   │   ├── category_schema.py
│   │   ├── product_schema.py
│   │   └── inventory_schema.py
│   │
│   ├── routers/
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   └── inventory_routes.py
│   │
│   ├── services/
│   │   ├── category_service.py
│   │   ├── product_service.py
│   │   └── inventory_service.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 11. Key Features

- Independent product catalog microservice
- Separate MySQL database
- JWT-based authentication
- Role-based access control
- Product and category management
- Product search and filtering
- Pagination and sorting
- Inventory stock-in and stock-out
- Inventory transaction history
- Low-stock identification
- Database constraints
- Alembic database migrations
- Docker deployment

## 12. Project Status

This README documents the intended service architecture and implemented API structure. Deployment and runtime behavior must be confirmed separately.
