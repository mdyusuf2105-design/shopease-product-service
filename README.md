# ShopEase – E-Commerce Microservices

ShopEase is organized as three independent FastAPI microservices in one Git repository.

## Services

| Service | Purpose | Local API URL | Swagger |
|---|---|---|---|
| Product Service | Product creation, listing, retrieval, update and deletion | http://localhost:8003 | http://localhost:8003/docs |
| Authentication Service | Registration, login, JWT verification and password changes | http://localhost:8002 | http://localhost:8002/docs |
| User Management Service | Authenticated user profiles and delivery addresses | http://localhost:8004 | http://localhost:8004/docs |

## Technology

- Python and FastAPI
- Pydantic request/response schemas
- SQLAlchemy ORM
- MySQL databases
- Alembic migrations (Auth and User services)
- JWT bearer authentication (Auth and User services)
- Docker and Docker Compose

## Repository layout

```text
ShopEase/
├── product-service/
├── auth-service/
├── user-service/
├── postman/
└── README.md
```

## Run the services

Each service has its own Docker Compose configuration and environment file. From the repository root, start one service at a time:

```bash
cd product-service
docker compose up --build -d
```

```bash
cd ../auth-service
docker compose up --build -d
```

```bash
cd ../user-service
docker compose up --build -d
```

Check each service's own README and `.env.example` for required configuration. Create a local `.env` from the example and supply your own values before starting containers. Do not commit `.env` files, database passwords, or JWT secrets.

## API documentation

FastAPI Swagger UI is available at `/docs` on each service's local port. OpenAPI JSON is available at `/openapi.json`.

## Authentication flow

1. Register an account through Authentication Service.
2. Log in to receive a bearer access token.
3. In Postman, save the returned token in the `authToken` collection variable.
4. Send the token as `Authorization: Bearer <token>` to User Management Service.
5. User Management Service validates the JWT using the shared signing secret and reads the `sub` claim as the Authentication Service user ID.

User Management does not provide a second registration or login system.

## Postman

Import the three JSON files in the `postman/` directory into Postman:

- `ShopEase-Product-Service.postman_collection.json`
- `ShopEase-Authentication-Service.postman_collection.json`
- `ShopEase-User-Management-Service.postman_collection.json`

The collections contain request templates. Replace example values and set the token variable after login. Importing a collection does not execute requests.

## Important notes

- The Product Service route prefix is `/api/products`.
- The Authentication Service route prefix is `/api/auth`.
- The User Management Service route prefixes are `/api/users/profile` and `/api/users/addresses`.
- Product IDs are UUIDs. Address and local profile IDs are integers.
- The Product Service routes shown in the collection do not declare bearer authentication in the supplied route definitions.
- The User Management Service requires a valid bearer token for profile and address operations.
- The Auth and User services must use matching JWT signing configuration for token validation.
- This documentation and the Postman collections describe request definitions; they do not claim that API requests have been executed or runtime behavior has been verified.
