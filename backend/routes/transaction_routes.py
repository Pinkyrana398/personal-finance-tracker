from flask import Blueprint, request, jsonify, session
from sqlalchemy import text

from extensions import db

transaction_bp = Blueprint('transactions', __name__)

def require_login():
    """Helper — returns user_id if logged in, else None"""
    return session.get('user_id', None)


@transaction_bp.route('/transactions', methods=['POST'])
def add_transaction():
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized — please login'}), 401

    data = request.get_json()
    type_ = data.get('type')          # 'income' or 'expense'
    category = data.get('category')
    amount = data.get('amount')
    note = data.get('note', '')
    date = data.get('date')

    if not all([type_, category, amount, date]):
        return jsonify({'error': 'type, category, amount, and date are required'}), 400

    if type_ not in ['income', 'expense']:
        return jsonify({'error': 'type must be income or expense'}), 400

    try:
        with db.engine.connect() as conn:
            result = conn.execute(text(
                """INSERT INTO transactions (user_id, type, category, amount, note, date)
                   VALUES (:user_id, :type, :category, :amount, :note, :date)
                   RETURNING id"""
            ), {
                "user_id": user_id,
                "type": type_,
                "category": category,
                "amount": float(amount),
                "note": note,
                "date": date
            })
            new_id = result.fetchone()[0]
            conn.commit()

        return jsonify({'message': 'Transaction added successfully', 'id': new_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized — please login'}), 401

    with db.engine.connect() as conn:
        result = conn.execute(text(
            """SELECT id, type, category, amount, note, date
               FROM transactions
               WHERE user_id = :user_id
               ORDER BY date DESC, created_at DESC"""
        ), {"user_id": user_id})
        rows = result.fetchall()

    transactions = [
        {
            'id': row[0],
            'type': row[1],
            'category': row[2],
            'amount': float(row[3]),
            'note': row[4] or '',
            'date': str(row[5])
        }
        for row in rows
    ]

    return jsonify(transactions), 200

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    with db.engine.connect() as conn:
        # IMPORTANT: always filter by user_id so users can't delete others' data
        result = conn.execute(text(
            "DELETE FROM transactions WHERE id = :id AND user_id = :user_id"
        ), {"id": transaction_id, "user_id": user_id})
        conn.commit()
        deleted_count = result.rowcount

    if deleted_count == 0:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify({'message': 'Transaction deleted'}), 200


@transaction_bp.route('/summary', methods=['GET'])
def get_summary():
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    with db.engine.connect() as conn:
        income_result = conn.execute(text(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = :uid AND type = 'income'"
        ), {"uid": user_id})
        total_income = float(income_result.scalar())

        expense_result = conn.execute(text(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = :uid AND type = 'expense'"
        ), {"uid": user_id})
        total_expense = float(expense_result.scalar())

    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense
    }), 200


@transaction_bp.route('/chart/category', methods=['GET'])
def chart_by_category():
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    with db.engine.connect() as conn:
        result = conn.execute(text(
            """SELECT category, SUM(amount) as total
               FROM transactions
               WHERE user_id = :uid AND type = 'expense'
               GROUP BY category
               ORDER BY total DESC"""
        ), {"uid": user_id})
        rows = result.fetchall()

    return jsonify([{'category': r[0], 'total': float(r[1])} for r in rows]), 200


@transaction_bp.route('/chart/monthly', methods=['GET'])
def chart_monthly():
    user_id = require_login()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    with db.engine.connect() as conn:
        # PostgreSQL date formatting uses TO_CHAR instead of DATE_FORMAT
        result = conn.execute(text(
            """SELECT TO_CHAR(date, 'YYYY-MM') as month, SUM(amount) as total
               FROM transactions
               WHERE user_id = :uid AND type = 'expense'
               GROUP BY month
               ORDER BY month DESC
               LIMIT 6"""
        ), {"uid": user_id})
        rows = result.fetchall()

    # Reverse so oldest month is first (left to right on chart)
    data = [{'month': r[0], 'total': float(r[1])} for r in rows]
    data.reverse()

    return jsonify(data), 200