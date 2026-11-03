# ShopEase Product Management Microservice

## Overview
Independent Product Management REST API using FastAPI and Docker.

## Technology Stack
- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- Docker

## Architecture
- Routers: API endpoints
- Schemas: Request and response validation
- Models: Product data structure
- Services: Business logic
- Config: Application settings
- Main: FastAPI initialization

## Project Structure
app/main.py
app/routers/product_routes.py
app/schemas/product_schema.py
app/models/product_model.py
app/services/product_service.py
app/config/settings.py
Dockerfile
.dockerignore
requirements.txt
.env

## Installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Local Execution
uvicorn app.main:app --reload --port 8003

## Docker Build
docker build -t shopease-product-service .

## Docker Run
docker run -d --name shopease-product-container -p 8003:8003 shopease-product-service

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/products/ | Create product |
| GET | /api/products/ | Get all products |
| GET | /api/products/{product_id} | Get product |
| PUT | /api/products/{product_id} | Update product |
| DELETE | /api/products/{product_id} | Delete product |
| GET | /health | Health check |

## Example Product
{
  "name": "Wireless Mouse",
  "description": "Wireless optical mouse",
  "price": 799.99,
  "stock_quantity": 50,
  "category": "Electronics",
  "status": "Active"
}

## Filtering and Pagination
/api/products/?category=Electronics&skip=0&limit=10

## Validation
Product name and category are required.
Price must be greater than zero.
Stock must be non-negative.
Status must be Active or Inactive.

## Error Handling
400: Invalid product ID
404: Product not found
422: Validation error
500: Internal server error

## Storage
Products are stored in an in-memory Python dictionary.
Data resets when the application restarts.

## Swagger Documentation
http://localhost:8003/docs
