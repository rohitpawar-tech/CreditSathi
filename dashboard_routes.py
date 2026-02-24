from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.score_service import ScoreService
from app.models.sale import Sale
from app.models.expense import Expense

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    # Get Score
    score_data = ScoreService.calculate_user_score(user_id)
    
    # Recent Transactions (Limit 5)
    recent_sales = Sale.query.filter_by(user_id=user_id).order_by(Sale.date.desc()).limit(3).all()
    recent_expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).limit(3).all()
    
    transactions = []
    for s in recent_sales:
        d = s.to_dict()
        d['type'] = 'sale'
        transactions.append(d)
    for e in recent_expenses:
        d = e.to_dict()
        d['type'] = 'expense'
        transactions.append(d)
        
    # Sort by date
    transactions.sort(key=lambda x: x['date'], reverse=True)

    return jsonify({
        "score": score_data,
        "recent_transactions": transactions
    })