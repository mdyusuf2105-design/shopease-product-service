# ShopEase Authentication Service

**Default local URL:** `http://localhost:8002`  
**Swagger:** `http://localhost:8002/docs`

## Endpoints

| Method | Path | Purpose | Authentication |
|---|---|---|---|
| GET | `/` | Service status | No |
| GET | `/health` | Health response | No |
| POST | `/api/auth/register` | Register an account | No |
| POST | `/api/auth/login` | Log in and receive JWT | No |
| GET | `/api/auth/me` | Get current account | Bearer token |
| POST | `/api/auth/verify-token` | Verify token and return user ID/role | Bearer token |
| POST | `/api/auth/change-password` | Change current password | Bearer token |

## Registration body

```json
{
  "full_name": "Example User",
  "email": "example@example.com",
  "password": "Example123",
  "confirm_password": "Example123"
}
```

The supplied schema requires a password of 8–128 characters containing at least one uppercase letter, one lowercase letter and one number. Password confirmation must match.

## Login body

```json
{
  "email": "example@example.com",
  "password": "Example123"
}
```

A successful login returns `access_token`, `token_type` and the user object. Use the access token as a bearer token for protected routes.

## Change password body

```json
{
  "current_password": "Example123",
  "new_password": "NewExample456"
}
```

The new password must be 8–128 characters and contain uppercase, lowercase and numeric characters.

See the service's Docker Compose file and `.env.example` for local configuration. Never commit the real `.env` or JWT signing secret.
