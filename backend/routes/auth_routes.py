from flask import Blueprint, request, jsonify, session
from sqlalchemy import text
from extensions import db
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        with db.engine.connect() as conn:
            conn.execute(text(
                "INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :hash)"
            ), {"username": username, "email": email, "hash": password_hash.decode('utf-8')})
            conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception:
        return jsonify({'error': 'Username or email already exists'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    with db.engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, username, email, password_hash FROM users WHERE email = :email"),
            {"email": email}
        )
        user = result.fetchone()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    stored_hash = user[3]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return jsonify({
            'message': 'Login successful',
            'user': {'id': user[0], 'username': user[1], 'email': user[2]}
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify({'id': session['user_id'], 'username': session['username']}), 200