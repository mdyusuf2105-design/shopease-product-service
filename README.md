# ShopEase – Product Management Microservice

## Project Overview
A RESTful Product Management API developed using FastAPI.

## Technology Stack
- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Docker
- Docker Compose

## Features
- Create products
- Retrieve all products
- Retrieve products by ID
- Update products
- Delete products
- Category filtering
- Pagination
- Input validation
- Error handling
- UUID-based product identification
- In-memory storage
- Docker deployment

## Project Structure
- app/main.py
- app/models/product_model.py
- app/schemas/product_schema.py
- app/routers/product_routes.py
- app/services/product_service.py
- app/config/settings.py
- Dockerfile
- docker-compose.yml
- requirements.txt

## Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003

## Run Using Docker
docker compose up -d --build

## Stop Docker
docker compose down

## API Documentation
http://localhost:8003/docs

## Health Check
http://localhost:8003/health

## API Endpoints

| Method | Endpoint | Description |
| POST | /api/products/ | Create product |
| GET | /api/products/ | List products |
| GET | /api/products/{product_id} | Get product |
| PUT | /api/products/{product_id} | Update product |
| DELETE | /api/products/{product_id} | Delete product |

## Storage
Products are stored in an in-memory Python dictionary. Data is not persistent after application restart.

## Deployment
The application is containerized using Docker and configured through Docker Compose.
