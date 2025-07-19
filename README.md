# Jarvis Backend with Authentication

This FastAPI backend now includes JWT token-based authentication.

## Features

- JWT token-based authentication
- Protected endpoints
- User management
- CORS support
- Password hashing with bcrypt

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

## Authentication Endpoints

### Login
- **POST** `/token`
- **Body**: `{"username": "testuser", "password": "secret"}`
- **Response**: `{"access_token": "...", "token_type": "bearer"}`

### Get Current User
- **GET** `/users/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User information

## Protected Endpoints

### Get Response (Protected)
- **POST** `/get_res`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"message": "your message"}`
- **Response**: Authenticated response with user info

## Default Test User

- **Username**: `testuser`
- **Password**: `secret`

## Example Usage

### 1. Get Access Token
```bash
curl -X POST "http://127.0.0.1:8000/token" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "secret"}'
```

### 2. Use Token for Protected Endpoints
```bash
curl -X POST "http://127.0.0.1:8000/get_res" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_token_here>" \
     -d '{"message": "Hello from authenticated client!"}'
```

### 3. Get User Info
```bash
curl -X GET "http://127.0.0.1:8000/users/me" \
     -H "Authorization: Bearer <your_token_here>"
```

## Testing

Run the test script to see the authentication flow:
```bash
python test_auth.py
```

## Security Notes

1. **Change the SECRET_KEY** in `auth/auth.py` for production
2. **Use environment variables** for sensitive configuration
3. **Use a real database** instead of the fake users database
4. **Implement proper user registration** and password reset
5. **Add rate limiting** for login attempts
6. **Use HTTPS** in production

## Token Information

- **Algorithm**: HS256
- **Expiry**: 30 minutes
- **Type**: Bearer token

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `401`: Unauthorized (invalid token or credentials)
- `400`: Bad request (inactive user)
- `422`: Validation error
