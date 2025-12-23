# 🚀 Quick Start Guide

## Getting Started (30 seconds)

### Option 1: Using Batch Files (Easiest)

1. **Start Backend:**
   - Double-click `start-backend.bat`
   - Wait for message: "Running on http://127.0.0.1:5000"

2. **Start Frontend:**
   - Double-click `start-frontend.bat`
   - Browser will open automatically at http://localhost:8000

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd d:\lenden-club-assign\backend
venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd d:\lenden-club-assign\frontend
python -m http.server 8000
```

Then open: http://localhost:8000

## 📝 Quick Test

1. **Register** two users (e.g., "alice" and "bob")
2. **Login** as alice (default balance: $1000)
3. **Transfer** $100 to bob
4. **View History** - see the transaction
5. **Logout** and login as bob
6. **Check Balance** - should be $1100

## 🔑 API Quick Reference

| Endpoint | Method | Auth Required |
|----------|--------|---------------|
| `/register` | POST | No |
| `/login` | POST | No |
| `/balance` | GET | Yes |
| `/transfer` | POST | Yes |
| `/transactions/:id` | GET | Yes |
| `/users` | GET | Yes |

## 🎯 Key Features Demonstrated

✅ JWT Authentication  
✅ Database Transactions (ACID)  
✅ Audit Logging  
✅ Real-time Balance Updates  
✅ Sortable Transaction History  
✅ Error Handling (insufficient funds, invalid receiver)  

## 🐛 Troubleshooting

**Backend won't start?**
- Make sure port 5000 is free
- Check that virtual environment is activated

**Frontend can't connect?**
- Verify backend is running on port 5000
- Check browser console for errors

**Database errors?**
- Delete `transactions.db` and restart backend
- Database will be recreated automatically

## 📊 Project Structure

```
lenden-club-assign/
├── backend/
│   ├── venv/              # Virtual environment
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Python dependencies
│   └── transactions.db    # SQLite database (auto-created)
├── frontend/
│   ├── index.html         # Login/Register page
│   ├── dashboard.html     # Main dashboard
│   ├── styles.css         # Styling
│   ├── auth.js           # Authentication logic
│   └── dashboard.js      # Dashboard logic
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
└── .gitignore           # Git ignore rules
```

Happy coding! 🎉
