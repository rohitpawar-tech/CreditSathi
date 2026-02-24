from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.sale import Sale
from app.models.expense import Expense

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales():
    user_id = get_jwt_identity()
    sales = Sale.query.filter_by(user_id=user_id).all()
    return jsonify([s.to_dict() for s in sales])

@finance_bp.route('/sales', methods=['POST'])
@jwt_required()
def add_sale():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_sale = Sale(
        user_id=user_id,
        amount=data['amount'],
        description=data['description'],
        date=data['date']
    )
    db.session.add(new_sale)
    db.session.commit()
    return jsonify(new_sale.to_dict()), 201

@finance_bp.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([e.to_dict() for e in expenses])

@finance_bp.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_expense = Expense(
        user_id=user_id,
        amount=data['amount'],
        description=data['description'],
        date=data['date']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(new_expense.to_dict()), 201

@finance_bp.route('/transaction/<int:type_id>/<string:t_type>', methods=['DELETE'])
@jwt_required()
def delete_transaction(type_id, t_type):
    user_id = get_jwt_identity()
    if t_type == 'sale':
        item = Sale.query.filter_by(id=type_id, user_id=user_id).first()
    else:
        item = Expense.query.filter_by(id=type_id, user_id=user_id).first()
        
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"message": "Not found"}), 404