# ShopEase – Microservices-Based E-Commerce Management System

ShopEase is a microservices-based e-commerce backend project built using Python, FastAPI, MySQL and Docker.

## Microservices

### 1. Product Management Service
- Product CRUD operations
- FastAPI
- Docker
- Port: 8003

Folder: `product-service/`

### 2. Authentication Service
- User registration and login
- Argon2 password hashing
- JWT authentication
- MySQL and Alembic
- Docker
- Port: 8002

Folder: `auth-service/`

### 3. User Management Service
- Customer profile management
- Profile CRUD operations
- Delivery address management
- Default address management
- JWT authentication integration
- MySQL and Alembic
- Docker
- Port: 8004

Folder: `user-service/`

## Project Structure

```text
ShopEase/
├── product-service/
├── auth-service/
├── user-service/
└── README.md
```

## Running the Microservices

Each service has its own Docker Compose configuration and database.

### Product Service

```bash
cd product-service
docker compose up -d --build
```

### Authentication Service

```bash
cd auth-service
docker compose up -d --build
```

### User Management Service

```bash
cd user-service
docker compose up -d --build
```

## API Documentation

| Service | Swagger URL |
|---|---|
| Product | http://localhost:8003/docs |
| Authentication | http://localhost:8002/docs |
| User Management | http://localhost:8004/docs |

## Database Separation

- Product Service: Independent database configuration.
- Authentication Service: `shopease_auth_db`.
- User Management Service: `shopease_user_db`.

## Security

- JWT-based authentication.
- Argon2 password hashing in Authentication Service.
- User-level profile and address authorization.
- Environment variables for sensitive configuration.
- `.env` files excluded from Git.

## Repository

ShopEase – Microservices-Based E-Commerce Management System.
