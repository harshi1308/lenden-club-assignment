# Money Transfer System 

A peer-to-peer money transfer system with real-time transaction tracking and audit logging.

## Project Overview

This project implements a **secure peer-to-peer money transfer system** with JWT-based authentication and ACID-compliant transactions. The system allows users to register accounts, login securely, transfer money to other users, and view their transaction history with sorting capabilities.

### Implementation Approach:
- **Backend:** RESTful API built with Flask, using SQLAlchemy ORM for database operations and JWT for stateless authentication
- **Frontend:** Single-page application using vanilla JavaScript with dynamic rendering and real-time balance updates
- **Database:** SQLite with proper foreign key constraints and transaction isolation
- **Security:** Password hashing with Werkzeug, JWT token-based authentication, and CORS-enabled API
- **Transaction Safety:** ACID-compliant transfers with automatic rollback on failures

### Key Features:
- User Authentication (JWT-based)
- Real-time Money Transfers
- ACID-compliant Database Transactions
- Immutable Audit Log System
- Transaction History with Sorting
- Real-time Balance Updates

### Technology Stack:

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- SQLite (Database)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript

---

## Setup/Run Instructions

### Prerequisites:
- Python 3.8 or higher
- Git

### Step-by-Step Setup:

#### 1. Clone the Repository:
```bash
git clone https://github.com/harshi1308/lenden-club-assignment.git
cd lenden-club-assignment
```

#### 2. Backend Setup:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt
```

#### 3. Run the Backend Server:
```bash
python app.py
```
The backend will start on `http://127.0.0.1:5000`

#### 4. Run the Frontend (Open New Terminal):
```bash
cd frontend
python -m http.server 8000
```
The frontend will be available at `http://localhost:8000`

#### 5. Access the Application:
Open your browser and navigate to `http://localhost:8000`

### Quick Start (Windows):
Alternatively, you can use the provided batch files:
1. Double-click `start-backend.bat` to start the backend
2. Double-click `start-frontend.bat` to start the frontend

---

## API Documentation

### Base URL: `http://127.0.0.1:5000`

### Authentication Endpoints:

#### 1. Register User
- **Endpoint:** `POST /register`
- **Auth Required:** No
- **Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```
- **Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "balance": 1000.0
  }
}
```

#### 2. Login
- **Endpoint:** `POST /login`
- **Auth Required:** No
- **Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```
- **Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "balance": 1000.0
  }
}
```

### Protected Endpoints:

#### 3. Get Balance
- **Endpoint:** `GET /balance`
- **Auth Required:** Yes (Bearer Token)
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
```json
{
  "username": "john_doe",
  "balance": 1000.0
}
```

#### 4. Transfer Money
- **Endpoint:** `POST /transfer`
- **Auth Required:** Yes (Bearer Token)
- **Request Body:**
```json
{
  "receiver_id": 2,
  "amount": 100.0,
  "description": "Payment for services"
}
```
- **Response:**
```json
{
  "message": "Transfer successful",
  "transaction": {
    "id": 1,
    "amount": 100.0,
    "receiver": "jane_doe",
    "timestamp": "2025-12-23T11:30:00Z"
  },
  "new_balance": 900.0
}
```

#### 5. Get Transaction History
- **Endpoint:** `GET /transactions/<user_id>`
- **Auth Required:** Yes (Bearer Token)
- **Response:**
```json
{
  "transactions": [
    {
      "id": 1,
      "type": "sent",
      "amount": 100.0,
      "other_party": "jane_doe",
      "timestamp": "2025-12-23T11:30:00Z",
      "status": "SUCCESS",
      "description": "Payment for services"
    }
  ]
}
```

#### 6. Get All Users
- **Endpoint:** `GET /users`
- **Auth Required:** Yes (Bearer Token)
- **Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "john_doe"
    },
    {
      "id": 2,
      "username": "jane_doe"
    }
  ]
}
```

---

## Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Unique, Not Null |
| email | String(120) | Unique, Not Null |
| password_hash | String(200) | Not Null |
| balance | Float | Default: 1000.0 |
| created_at | DateTime | Default: UTC Now |

### AuditLog Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| sender_id | Integer | Foreign Key (User), Not Null |
| receiver_id | Integer | Foreign Key (User), Not Null |
| amount | Float | Not Null |
| status | String(20) | Not Null (SUCCESS/FAILED) |
| timestamp | DateTime | Default: UTC Now |
| description | String(200) | Optional |

### Database Relationships:
- **Users ↔ AuditLog:** One-to-Many relationship
  - Each user can have multiple transactions as sender (sender_id → User.id)
  - Each user can have multiple transactions as receiver (receiver_id → User.id)
- **Foreign Keys:** AuditLog.sender_id and AuditLog.receiver_id reference User.id
- **Cascade Rules:** ON DELETE CASCADE for user deletions

---

## ACID Compliance

The transfer endpoint implements ACID properties:
- Atomicity: Both debit and credit operations happen together or not at all
- Consistency: Balance constraints are maintained (no negative balances)
- Isolation: SQLite transactions prevent race conditions
- Durability: Committed transactions are permanently stored

Implementation:
```python
try:
    sender.balance -= amount
    receiver.balance += amount
    db.session.commit()  # Both succeed
except:
    db.session.rollback()  # Both fail
```

---

## AI Tool Usage Log (MANDATORY)

### AI-Assisted Tasks:

#### 1. **Flask Application Structure & Initial Setup**
   - Generated Flask application boilerplate with proper configuration
   - Set up SQLAlchemy database models with relationships
   - Configured CORS for cross-origin requests
   - **Result:** Complete working backend structure in minutes instead of hours

#### 2. **Database Transaction Implementation with ACID Properties**
   - Generated SQLAlchemy transaction wrapper with commit/rollback logic
   - Created error handling for edge cases (insufficient balance, invalid receiver)
   - Implemented concurrent transaction safety with database-level locks
   - **Result:** Rock-solid transaction logic that prevents race conditions

#### 3. **JWT Authentication System**
   - Generated Flask-JWT-Extended configuration and initialization
   - Created login endpoint with JWT token generation
   - Implemented @jwt_required() decorators for protected routes
   - Generated token validation and user identity extraction logic
   - **Result:** Secure authentication working on first attempt

#### 4. **RESTful API Endpoint Development**
   - Generated all CRUD endpoints for user management
   - Created transfer endpoint with validation logic
   - Built transaction history endpoint with filtering
   - Generated consistent error response format across all endpoints
   - **Result:** Complete API with proper HTTP status codes and error handling

---

### Effectiveness Score: **4/5**

#### Justification:

**What Worked Exceptionally Well (3-4 hours saved):**
- **Flask Application Setup:** AI generated a complete Flask application structure with proper configuration, SQLAlchemy models, and CORS setup. This saved approximately 1 hour of boilerplate coding and configuration research.
  
- **Database Transactions:** AI-generated ACID-compliant logic was production-ready with zero modifications. Understanding and implementing proper rollback handling manually would have taken 1-2 hours of research and testing.
  
- **JWT Authentication:** The authentication system worked perfectly on the first try. Setting up JWT from scratch typically requires reading documentation, handling edge cases, and debugging token issues - saved approximately 2 hours.

- **API Structure:** All endpoints were generated with proper error handling, status codes, and consistent response format. This level of completeness usually requires multiple iterations - saved approximately 1 hour.

**Minor Refinements Needed (~20 minutes spent):**
- Some error messages were too technical and needed to be made more user-friendly
- A few variable names required adjustments for better code readability
- Database schema relationships needed minor optimization for foreign key behavior

**Why Not 5/5:**
- Still needed to understand the generated code thoroughly before using it in production
- Had to manually test all API endpoints to ensure proper integration
- Required human oversight to verify security implementations
- Some edge cases in validation logic needed manual additions

**Overall Impact:**
The AI tools accelerated backend development by approximately 75-80%, transforming what would have been a 4-5 hour coding session into about 1 hour of work. The generated code was robust and required minimal debugging. The biggest value was in avoiding repetitive boilerplate code and reducing time spent reading documentation for Flask, SQLAlchemy, and JWT libraries.



