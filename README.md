# Portkey 🔐

Portkey is a lightweight authentication and SSO starter built with
FastAPI, Strawberry GraphQL, SQLAlchemy, and Next.js.

It provides a simple foundation for building apps that need authentication,
OAuth login, and a modern API layer without the complexity of large auth frameworks.

Plug it in, customize it, ship it.

---

## Tech Stack

**Backend:** FastAPI, Strawberry GraphQL, SQLAlchemy, SQLite → PostgreSQL  
**Frontend:** Next.js, React, Apollo Client, Tailwind CSS  
**Auth:** JWT, Argon2 (Passlib), OAuth (v3)
**Testing:** Pytest, Jest, React Testing Library  
**Deployment:** (coming in v3)

---
## Architecture

        Next.js Client
                │
                ▼
        GraphQL API
                │
                ▼
        FastAPI + Strawberry
                │
                ▼
        Authentication Layer
                │
                ▼
        SQLAlchemy ORM
                │
                ▼
        SQLite (dev) / PostgreSQL (prod)

---
## Roadmap

### V1 — Core API
- [x] Project setup and folder structure
- [x] FastAPI app entry point
- [x] SQLAlchemy + SQLite setup and User model
- [x] Password hashing with Argon2
- [x] Register mutation
- [x] Login mutation with JWT access + refresh token
- [x] Logout mutation
- [x] Refresh token endpoint
- [x] Protected `me` query with JWT auth guard
- [x] Input validation and error handling
- [ ] Rate limiting on auth endpoints
- [ ] Pytest tests for all auth endpoints
- [x] .env.example with all required variables
- [ ] README setup instructions for API

### V2 — Frontend
- [x] Next.js project setup in /client
- [ ] Apollo Client setup connected to GraphQL API
- [ ] Register page and form
- [ ] Login page and form
- [ ] Protected dashboard page showing current user
- [ ] Logout functionality
- [ ] Basic error handling on forms
- [ ] Component tests

### V3 — Open Source Ready
- [ ] Email verification on signup
- [ ] Password reset flow
- [ ] RBAC
- [ ] Google OAuth
- [ ] GitHub OAuth
- [ ] Migrate SQLite to PostgreSQL
- [ ] Docker and docker-compose setup
- [ ] One command local setup
- [ ] Postman collection export
- [ ] Contributing guide
- [ ] License file

---

## Project Structure

    portkey/
    ├── api/                        
    │   ├── main.py                 
    │   ├── schema.py               
    │   ├── database.py             
    │   ├── resolvers/              
    │   │   ├── auth.py             
    │   │   └── user.py             
    │   ├── services/               
    │   │   ├── auth_service.py     
    │   │   └── user_service.py     
    │   ├── models/
    │   │   └── user.py             
    │   ├── middleware/             
    │   └── tests/                  
    │       ├── test_auth.py
    │       └── test_user.py
    ├── client/                     
    │   ├── app/
    │   │   ├── page.tsx            
    │   │   ├── register/
    │   │   └── dashboard/
    │   ├── components/
    │   └── lib/
    ├── .env.example
    ├── docker-compose.yml
    └── README.md

---

## Quick Start

### Prerequisites
- Python 3.12
- Git

---

### 1. Clone the repo
```bash
git clone https://github.com/somir1/portkey.git
cd portkey
```

### 2. Set up your virtual environment
```bash
cd api
python3.12 -m venv .venv
source .venv/bin/activate
```
Windows:
```bash
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp ../.env.example .env
```
Open `api/.env` and update:
```bash
DATABASE_URL=sqlite+aiosqlite:///./dev.db
JWT_SECRET_KEY=your-long-random-secret-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
APP_ENV=development
APP_PORT=8000
```

### 5. Start the server
```bash
uvicorn main:app --reload
```

### 6. Open the playground
Visit `http://localhost:8000/graphql`

You should see the GraphiQL interface ready to go.
---

## Authentication Endpoints

## Register

Creates a new user account.

    mutation {
        register(
            email: "user@example.com"
            password: "Password123!"
            firstName: "John"
            lastName: "Doe"
        ) {
            accessToken
            refreshToken
            userId
            email
            firstName
            lastName
            }
    }

## What it does

    Creates a new user in the database
    Hashes the password using Argon2
    Generates JWT access and refresh tokens
    Stores the refresh token in the database
    Returns authentication tokens and user info

---

## Login

Authenticates an existing user.

    mutation {
        login(
            email: "user@example.com"
            password: "Password123!"
        ) {
            accessToken
            refreshToken
            userId
            email
            firstName
            lastName
        }
    }

## What it does

    Verifies the user's email and password
    Generates new access and refresh tokens
    Updates the stored refresh token
    Returns authentication tokens and user info

---

## Logout

Logs the current user out.

    mutation {
        logout {
            success
            message
        }
    }

    Headers
        Authorization: Bearer <access_token>     
## What it does

    Validates the user's JWT token
    Clears the stored refresh token from the database
    Invalidates the current login session

---
## Me

Returns the currently authenticated user.

    query {
        me {
            id
            email
            firstName
            lastName
        }
    }

    Headers
        Authorization: Bearer <access_token>     
## What it does

    Validates the JWT access token
    Loads the user from the database
    Returns the authenticated user's profile


## License

MIT
