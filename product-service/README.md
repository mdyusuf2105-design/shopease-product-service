# ShopEase Authentication Microservice

## 1. Project Overview

The ShopEase Authentication Microservice is an independent authentication service developed using FastAPI and MySQL. It provides secure user registration, login, JWT-based authentication, token verification, and password management.

This service is designed to integrate with other ShopEase microservices, including Product, Order, and User services.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming |
| FastAPI | REST API development |
| MySQL 8.0 | Database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| JWT | Token-based authentication |
| Argon2 | Password hashing |
| Pydantic | Request validation |
| Docker | Containerization |
| Docker Compose | Service orchestration |

## 3. Project Structure

```text
shopease-auth-service/
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
│   │   └── user_model.py
│   │
│   ├── schemas/
│   │   └── auth_schema.py
│   │
│   ├── routers/
│   │   └── auth_routes.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .dockerignore
├── .env
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 4. Features

- User registration with input validation.
- Unique email verification.
- Secure password hashing using Argon2.
- User login with email and password.
- JWT access token generation.
- Configurable JWT expiration.
- Protected endpoints using Bearer authentication.
- Current authenticated user details.
- JWT token verification.
- Password change functionality.
- Account activation and deactivation checks.
- MySQL database integration.
- Database migrations using Alembic.
- Docker containerization with Docker Compose.
- Persistent MySQL storage using Docker volumes.

## 5. Environment Configuration

Create a `.env` file in the project root.

Configure the following environment variables:

```env
APP_NAME=ShopEase Authentication Service
APP_VERSION=1.0.0
APP_PORT=8002

MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=shopease_auth_db
MYSQL_USER=shopease_user
MYSQL_PASSWORD=your_database_password

DATABASE_URL=mysql+pymysql://shopease_user:your_database_password@db:3306/shopease_auth_db

JWT_SECRET_KEY=your_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit the `.env` file or expose your JWT secret.

## 6. Installation and Execution

### Prerequisites

- Python 3.11+
- Docker Desktop or Colima
- Docker Compose

### Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd shopease-auth-service
```

### Start the application

```bash
docker compose up -d --build
```

This command builds the authentication service, starts the MySQL container, waits for the database health check, applies Alembic migrations, and starts FastAPI.

### Check running containers

```bash
docker compose ps
```

### View application logs

```bash
docker logs sh