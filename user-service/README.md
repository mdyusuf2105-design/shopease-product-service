# ShopEase User Management Service

**Default local URL:** `http://localhost:8004`  
**Swagger:** `http://localhost:8004/docs`

All profile and address routes require `Authorization: Bearer <access_token>`. The token is issued by ShopEase Authentication Service. This service verifies the JWT and uses its `sub` claim as `auth_user_id`; it does not create passwords or issue login tokens.

## Profile endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Service status |
| GET | `/health` | Health response |
| POST | `/api/users/profile` | Create profile |
| GET | `/api/users/profile` | Get current user's profile |
| PUT | `/api/users/profile` | Replace profile fields |
| PATCH | `/api/users/profile` | Partially update profile |
| DELETE | `/api/users/profile` | Delete profile |
| PATCH | `/api/users/profile/deactivate` | Deactivate profile |

Profile create/PUT body:

```json
{
  "full_name": "Example User",
  "phone_number": "+919876543210",
  "date_of_birth": "2000-05-21",
  "gender": "Prefer not to say",
  "profile_image": "https://example.com/profile.jpg"
}
```

All fields except `full_name` are optional. Phone number, when supplied, must contain 7–15 digits, optionally prefixed by `+`.

## Address endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/users/addresses` | Add address |
| GET | `/api/users/addresses` | List current user's addresses |
| GET | `/api/users/addresses/{address_id}` | Get one owned address |
| PUT | `/api/users/addresses/{address_id}` | Replace address fields |
| PATCH | `/api/users/addresses/{address_id}` | Partially update address |
| DELETE | `/api/users/addresses/{address_id}` | Delete address |
| PATCH | `/api/users/addresses/{address_id}/default` | Set default address |

Address create/PUT body:

```json
{
  "address_type": "Home",
  "full_name": "Example User",
  "phone_number": "+919876543210",
  "address_line_1": "12 Example Street",
  "address_line_2": "Near Main Road",
  "city": "Kumbakonam",
  "state": "Tamil Nadu",
  "country": "India",
  "postal_code": "612001",
  "is_default": true
}
```

`address_type` must be `Home`, `Office` or `Other`. Address update fields are optional for PATCH. Address IDs are integers.

## Ownership and default address behavior

Address operations are scoped to the authenticated user's profile. The service logic clears other default flags when setting a new default address. A profile is associated with the Authentication Service account through unique `auth_user_id`.

See the service's Docker Compose file and `.env.example` for local configuration. The user-service JWT secret and algorithm must match the Authentication Service configuration.
