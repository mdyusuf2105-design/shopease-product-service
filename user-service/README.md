# ShopEase User Management Microservice

## Overview

An independent FastAPI microservice for managing customer profiles and delivery addresses. It integrates with the ShopEase Authentication Service using JWT authentication.

## Technology Stack

- Python 3.11
- FastAPI
- MySQL 8.0
- SQLAlchemy
- Alembic
- JWT
- Pydantic
- Docker and Docker Compose

## Features

- Create, retrieve, update and delete user profiles.
- Partial profile updates.
- Profile deactivation.
- Create and manage multiple delivery addresses.
- Retrieve individual addresses.
- Set a default delivery address.
- Ensure only one default address per profile.
- JWT authentication using the existing Authentication Service secret.
- User-level resource ownership protection.

## Database

Database: `shopease_user_db`

Tables:
- `user_profiles`
- `user_addresses`

The `auth_user_id` field identifies the user in the Authentication Service. Passwords and authentication credentials are not stored here.

## Environment Variables

Configure these values in `.env`:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `APP_NAME`
- `APP_VERSION`
- `APP_PORT`

Use the same JWT secret and algorithm as the Authentication Service.

Never commit `.env` to GitHub.

## Run with Docker

```bash
docker compose up -d --build
```

Stop containers:

```bash
docker compose down
```

The named MySQL volume preserves database data.

## API Documentation

Base URL: `http://localhost:8004`

Swagger UI: `http://localhost:8004/docs`

ReDoc: `http://localhost:8004/redoc`

## Profile APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/profile` | Create profile |
| GET | `/api/users/profile` | Get current profile |
| PUT | `/api/users/profile` | Update profile |
| PATCH | `/api/users/profile` | Partially update profile |
| DELETE | `/api/users/profile` | Delete profile |
| PATCH | `/api/users/profile/deactivate` | Deactivate profile |

## Address APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/addresses` | Add address |
| GET | `/api/users/addresses` | List addresses |
| GET | `/api/users/addresses/{address_id}` | Get address |
| PUT | `/api/users/addresses/{address_id}` | Update address |
| PATCH | `/api/users/addresses/{address_id}` | Partially update address |
| DELETE | `/api/users/addresses/{address_id}` | Delete address |
| PATCH | `/api/users/addresses/{address_id}/default` | Set default address |

## Authentication

Protected endpoints require:

`Authorization: Bearer <access_token>`

The token must be issued by the ShopEase Authentication Service. The User Service validates its signature and expiry using the shared JWT secret.

## Database Migrations

Apply existing migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "describe change"
```

## Service Ports

- Product Service: 8003
- Authentication Service: 8002
- User Management Service: 8004
- User MySQL host port: 3308

## Account Deactivation

Deactivating a profile changes only the User Service profile status. It does not deactivate or delete the corresponding Authentication Service account. The two services must coordinate account status through a separately defined integration workflow.
