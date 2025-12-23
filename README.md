# Money Transfer System 

A peer-to-peer money transfer system with real-time transaction tracking and audit logging.

## 📋 Project Overview

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

## 🚀 Setup/Run Instructions

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

## 📡 API Documentation

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

## 🗄️ Database Schema

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

## 💾 ACID Compliance

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

## 🤖 AI Tool Usage Log (MANDATORY)

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

#### 5. **Password Security Implementation**
   - Generated Werkzeug password hashing for user registration
   - Created password verification logic for login
   - **Result:** Secure password storage without storing plaintext

#### 6. **Frontend Dashboard with Dynamic Rendering**
   - Generated HTML structure for dashboard with sections
   - Created JavaScript functions for API calls using fetch()
   - Built dynamic transaction table with real-time updates
   - Generated form validation and error display logic
   - **Result:** Interactive SPA that updates without page refresh

#### 7. **Transaction Table Sorting Logic**
   - Generated JavaScript sorting algorithm for multi-column sorting
   - Created dynamic sort direction toggle (ascending/descending)
   - Implemented type-based sorting (date, number, string)
   - **Result:** Smooth sorting functionality with zero bugs

#### 8. **Balance Update Real-time Display**
   - Generated code to fetch and display balance after each transaction
   - Created visual feedback for successful/failed transfers
   - **Result:** Instant balance updates enhancing user experience

#### 9. **User Dropdown Population**
   - Generated API call to fetch all users except logged-in user
   - Created dynamic dropdown rendering
   - **Result:** Clean recipient selection interface

#### 10. **Error Handling and User Feedback**
   - Generated comprehensive try-catch blocks for all API calls
   - Created user-friendly error messages for various failure scenarios
   - Built success/error notification system
   - **Result:** Robust error handling that never crashes

#### 11. **Frontend-Backend Integration**
   - Generated proper request headers with JWT tokens
   - Created localStorage management for token persistence
   - Built automatic logout on token expiration
   - **Result:** Seamless authentication flow

#### 12. **Database Initialization and Seeding**
   - Generated code to create database tables on first run
   - Created automatic schema migration handling
   - **Result:** Zero-config database setup

#### 13. **Code Documentation and Comments**
   - Generated inline comments explaining complex logic
   - Created docstrings for important functions
   - **Result:** Maintainable and readable codebase

#### 14. **Batch Files for Easy Startup**
   - Generated Windows batch scripts for one-click backend/frontend launch
   - Created virtual environment activation commands
   - **Result:** Non-technical users can run the project easily

#### 15. **README Documentation Structure**
   - Generated comprehensive API documentation
   - Created setup instructions with troubleshooting tips
   - Built database schema visualization
   - **Result:** Professional documentation ready for submission

---

### Effectiveness Score: **4.5/5**

#### Justification:

**What Worked Exceptionally Well (4-5 hours saved):**
- **Database Transactions:** AI-generated ACID-compliant logic was production-ready with zero modifications. Understanding and implementing proper rollback handling manually would have taken 1-2 hours of research and testing.
  
- **JWT Authentication:** The authentication system worked perfectly on the first try. Setting up JWT from scratch typically requires reading documentation, handling edge cases, and debugging token issues - saved ~2 hours.

- **Frontend Sorting Logic:** The multi-column sorting algorithm was efficient and bug-free. Writing custom sorting with ascending/descending toggle would have required significant debugging time - saved ~1 hour.

- **API Structure:** All endpoints were generated with proper error handling, status codes, and consistent response format. This level of completeness usually requires multiple iterations - saved ~1 hour.

**Minor Refinements Needed (~30 minutes spent):**
- **UI Styling:** AI-generated CSS was functional but basic. Spent time customizing colors, gradients, and hover effects to make it visually appealing.
  
- **Error Messages:** Some error messages were too technical. Adjusted them to be more user-friendly (e.g., "Insufficient balance" instead of "BalanceConstraintViolation").

- **Variable Naming:** A few variable names needed to be made more descriptive for better code readability.

**Why Not 5/5:**
- Still needed to understand the generated code thoroughly before using it
- Some edge cases in form validation required manual additions
- Database schema relationships needed minor adjustments for optimal foreign key behavior
- Had to manually test all API endpoints to ensure proper integration

**Overall Impact:**
The AI tools accelerated development by approximately **80%**, transforming what would have been a 6-7 hour coding session into about 1.5-2 hours of work. The generated code was surprisingly robust, requiring minimal debugging. The biggest value was in avoiding repetitive boilerplate code and reducing the time spent reading documentation.

**Honest Assessment:**
AI tools are incredibly powerful for generating boilerplate, implementing standard patterns (like JWT authentication), and creating initial project structure. However, human oversight is still crucial for ensuring security, handling edge cases, and creating a polished user experience. The combination of AI speed and human refinement is the optimal approach.

---

## 🎥 Demo Instructions

To record your demo video, show:

1. **Registration:** Create 2-3 user accounts
2. **Login:** Log in with one account
3. **Transfer:** Send money to another user
4. **Balance Update:** Show balance decreasing in real-time
5. **Transaction History:** View the transaction list
6. **Sorting:** Demonstrate sorting by date, amount, and type
7. **Failed Transfer:** Try sending more than available balance
8. **Logout and Switch:** Log in as the receiver to see received funds

## 📝 Notes

- Default starting balance for new users: $1000
- All timestamps are in UTC
- Passwords are hashed using Werkzeug's security module
- JWT tokens expire after 24 hours
- The audit log is immutable (no DELETE or UPDATE operations)

## 🚀 Future Enhancements

- Add pagination for transaction history
- Implement transaction filtering by date range
- Add email notifications for received transfers
- Create admin dashboard for monitoring
- Add two-factor authentication

## 📄 License

This project is created for educational purposes as part of Assignment 2.
