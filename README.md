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
        │ GraphQL
        ▼
FastAPI + Strawberry
        │
Authentication Layer
        │
SQLAlchemy ORM
        │
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
- [ ] Refresh token endpoint
- [x] Protected `me` query with JWT auth guard
- [ ] Input validation and error handling
- [ ] Rate limiting on auth endpoints
- [ ] Pytest tests for all auth endpoints
- [x] .env.example with all required variables
- [ ] README setup instructions for API

### V2 — Frontend
- [ ] Next.js project setup in /client
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

Coming soon — setup instructions will be added when V1 is complete.

---

## License

MIT
