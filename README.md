# ShopEase – Microservices-Based E-Commerce Management System

ShopEase is a microservices-based e-commerce backend project developed using Python and FastAPI.

## Microservices

### 1. Product Service
- FastAPI
- Python
- Product CRUD APIs
- Docker

Location: `product-service/`

### 2. Authentication Service
- FastAPI
- MySQL 8.0
- SQLAlchemy
- Alembic
- JWT Authentication
- Argon2 Password Hashing
- Docker and Docker Compose

Location: `auth-service/`

## Project Structure

```text
ShopEase/
├── product-service/
│   ├── app/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
├── auth-service/
│   ├── app/
│   ├── alembic/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
└── README.md
