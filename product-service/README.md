# ShopEase Product Service

**Default local URL:** `http://localhost:8003`  
**Swagger:** `http://localhost:8003/docs`

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Service welcome |
| GET | `/health` | Health response |
| POST | `/api/products/` | Create a product |
| GET | `/api/products/` | List products; optional `category`, `skip`, `limit` |
| GET | `/api/products/{product_id}` | Retrieve a product by UUID |
| PUT | `/api/products/{product_id}` | Update a product |
| DELETE | `/api/products/{product_id}` | Delete a product (204 response) |

## Product request fields

`name` (1–100 characters), `description` (optional, up to 500 characters), `price` (greater than zero), `stock_quantity` (zero or greater), `category` (1–50 characters), and `status` (`Active` or `Inactive`, default `Active`).

The update schema inherits the create schema, so PUT expects the complete product payload.

## Example create request

```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse",
  "price": 799.0,
  "stock_quantity": 25,
  "category": "Electronics",
  "status": "Active"
}
```

## List query parameters

- `category`: optional, 1–50 characters
- `skip`: optional, integer >= 0; default 0
- `limit`: optional, integer 1–100; default 10

See the service's Docker Compose file and `.env.example` for local configuration.
