# Money Transfer System 

A peer-to-peer money transfer system with real-time transaction tracking and audit logging.

Features

- User Authentication (JWT-based)
- Real-time Money Transfers
- ACID-compliant Database Transactions
- Immutable Audit Log System
- Transaction History with Sorting
- Real-time Balance Updates

Technology Stack

Backend:
- Python 3.x
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- SQLite (Database)

Frontend:
- HTML5
- CSS3
- Vanilla JavaScript


Database Schema

 Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Unique, Not Null |
| email | String(120) | Unique, Not Null |
| password_hash | String(200) | Not Null |
| balance | Float | Default: 1000.0 |
| created_at | DateTime | Default: UTC Now |

AuditLog Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| sender_id | Integer | Foreign Key (User), Not Null |
| receiver_id | Integer | Foreign Key (User), Not Null |
| amount | Float | Not Null |
| status | String(20) | Not Null (SUCCESS/FAILED) |
| timestamp | DateTime | Default: UTC Now |
| description | String(200) | Optional |

ACID Compliance

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

## 🤖 AI Tool Usage Log

### Tasks Where AI Was Used:

1. **Database Transaction Implementation**
   - Used AI to generate Flask-SQLAlchemy transaction wrapper with proper rollback handling
   - Generated error handling for edge cases (insufficient balance, receiver not found)

2. **JWT Authentication Middleware**
   - Generated Flask-JWT-Extended configuration and decorators
   - Created token validation and user identity extraction logic

3. **Sortable Transaction Table**
   - Generated JavaScript sorting logic for transaction history
   - Created dynamic table rendering with type-based styling

4. **API Error Handling**
   - Generated comprehensive error responses for all endpoints
   - Created consistent error message format across API

5. **Frontend Form Validation**
   - Generated client-side validation logic
   - Created real-time error display functionality

### Effectiveness Score: 4.5/5

**Justification:**
- Saved approximately 4-5 hours on boilerplate code generation
- Authentication setup was nearly perfect and required minimal modifications
- Database transaction logic was solid and handled edge cases well
- Frontend sorting algorithm was efficient and bug-free
- Only minor refinements needed for UI styling and error messages

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
