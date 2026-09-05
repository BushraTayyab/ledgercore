# LedgerCore

### Concurrent Financial Transaction Ledger

LedgerCore is a backend financial ledger system built to explore
**database integrity, ACID transactions, authentication,
authorization, and concurrency control**.

The project focuses on building reliable financial operations where
balance updates and transaction records remain consistent even under
concurrent requests.

## Current Features

- User registration with password hashing
- JWT-based authentication
- Wallet creation
- Wallet ownership authorization
- Deposit and withdrawal operations
- PostgreSQL persistence
- ACID transaction handling
- Row-level locking for concurrent transactions
- Request validation
- Automated API, service, and security tests
- 38 passing tests

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Database Migrations:** Alembic
- **Authentication:** JWT
- **Password Hashing:** Argon2
- **Testing:** Pytest
- **Version Control:** Git & GitHub

## Architecture

LedgerCore follows a layered backend architecture:

```text
Client
   ↓
FastAPI API Layer
   ↓
Authentication & Authorization
   ↓
Service Layer
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL
```

## Database Design

LedgerCore uses three core entities:

- **Users** — stores user identity and authentication information.
- **Wallets** — represents a user's financial wallet and current balance.
- **Transactions** — records every deposit and withdrawal made against a wallet.

### Relationships

User
 │
 └───< Wallet
          │
          └───< Transaction

A user can have multiple wallets, and each wallet can have multiple transactions.

## API Endpoints

### User Registration

POST /users

Creates a new user account with a securely hashed password.

### User Login

POST /login

Authenticates a user and returns a JWT access token.

### Create Wallet

POST /users/{user_id}/wallets

Creates a new wallet for an existing user.

### Create Transaction

POST /wallets/{wallet_id}/transactions

Creates a deposit or withdrawal transaction.

Transactions require a valid JWT, and the authenticated user must own the requested wallet.

### Transaction Request

{
  "type": "deposit",
  "amount": "100"
}

### Successful Response

{
  "wallet_id": "TESTW001",
  "new_balance": 600,
  "transaction_id": "..."
}

## Authentication & Security

LedgerCore uses JWT-based authentication to protect financial transaction endpoints.

### Authentication Flow

1. A user registers with an email and password.
2. The password is securely hashed using Argon2 before being stored.
3. The user logs in using their email and password.
4. LedgerCore verifies the credentials and issues a JWT access token.
5. Protected endpoints require the token in the `Authorization` header.
6. The token identifies the authenticated user.
7. Wallet ownership is verified before allowing transactions.

### Authorization

Authentication determines **who the user is**, while authorization determines **what the user is allowed to access**.

For wallet transactions, LedgerCore verifies that the authenticated user owns the requested wallet before processing the transaction.

Unauthorized access attempts return `403 Forbidden`.

Invalid or missing authentication credentials are handled separately from authorization failures.

### Password Security

Passwords are never stored directly in the database. LedgerCore uses Argon2 password hashing to securely store password hashes.

### JWT

Access tokens contain the authenticated user's identifier and an expiration time.

Example:

Authorization: Bearer <access_token>

## Testing

LedgerCore uses Pytest for automated testing across the service, API, and security layers.

Current test suite:

38 tests passed

The tests cover:

- Deposit operations
- Withdrawal operations
- Invalid transaction amounts
- Invalid transaction types
- Insufficient balance
- Wallet-not-found scenarios
- User creation
- Wallet creation
- User authentication
- Password verification
- JWT creation and validation
- Expired and invalid JWTs
- Wallet ownership authorization
- Unauthorized wallet access

## Roadmap

The project is being developed incrementally with a focus on production-oriented backend engineering.

- [x] User authentication
- [x] JWT authorization
- [x] Wallet ownership checks
- [x] Atomic financial transactions
- [x] Row-level locking
- [x] Automated testing
- [ ] Idempotency keys
- [ ] Optimistic locking
- [ ] Concurrency testing
- [ ] Observability and structured logging
- [ ] Dockerization