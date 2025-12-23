from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=1000.0)  # Starting balance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # SUCCESS or FAILED
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user_id': user.id,
        'username': user.username,
        'balance': user.balance
    }), 200

@app.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return jsonify({'balance': user.balance}), 200

@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    sender_id = int(get_jwt_identity())
    data = request.get_json()
    
    receiver_username = data.get('receiver_username')
    amount = float(data.get('amount'))
    
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400
    
    # Start database transaction
    try:
        sender = User.query.get(sender_id)
        receiver = User.query.filter_by(username=receiver_username).first()
        
        if not receiver:
            # Log failed transaction
            log = AuditLog(
                sender_id=sender_id,
                receiver_id=0,
                amount=amount,
                status='FAILED',
                description=f'Receiver {receiver_username} not found'
            )
            db.session.add(log)
            db.session.commit()
            return jsonify({'error': 'Receiver not found'}), 404
        
        if sender.id == receiver.id:
            return jsonify({'error': 'Cannot transfer to yourself'}), 400
        
        if sender.balance < amount:
            # Log failed transaction
            log = AuditLog(
                sender_id=sender_id,
                receiver_id=receiver.id,
                amount=amount,
                status='FAILED',
                description='Insufficient balance'
            )
            db.session.add(log)
            db.session.commit()
            return jsonify({'error': 'Insufficient balance'}), 400
        
        # Perform transfer (ACID transaction)
        sender.balance -= amount
        receiver.balance += amount
        
        # Log successful transaction
        log = AuditLog(
            sender_id=sender_id,
            receiver_id=receiver.id,
            amount=amount,
            status='SUCCESS',
            description='Transfer completed'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Transfer successful',
            'new_balance': sender.balance,
            'transaction_id': log.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/transactions/<int:user_id>', methods=['GET'])
@jwt_required()
def get_transactions(user_id):
    current_user_id = int(get_jwt_identity())
    
    # Users can only view their own transactions
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all transactions where user is sender or receiver
    sent = AuditLog.query.filter_by(sender_id=user_id).all()
    received = AuditLog.query.filter_by(receiver_id=user_id).all()
    
    transactions = []
    
    for txn in sent:
        receiver = User.query.get(txn.receiver_id)
        transactions.append({
            'id': txn.id,
            'type': 'SENT',
            'other_party': receiver.username if receiver else 'Unknown',
            'amount': txn.amount,
            'status': txn.status,
            'timestamp': txn.timestamp.isoformat(),
            'description': txn.description
        })
    
    for txn in received:
        if txn.status == 'SUCCESS':  # Only show successful received transactions
            sender = User.query.get(txn.sender_id)
            transactions.append({
                'id': txn.id,
                'type': 'RECEIVED',
                'other_party': sender.username if sender else 'Unknown',
                'amount': txn.amount,
                'status': txn.status,
                'timestamp': txn.timestamp.isoformat(),
                'description': txn.description
            })
    
    # Sort by timestamp descending
    transactions.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({'transactions': transactions}), 200

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = int(get_jwt_identity())
    users = User.query.filter(User.id != current_user_id).all()
    return jsonify({
        'users': [{'id': u.id, 'username': u.username} for u in users]
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
