from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.score_service import ScoreService
from app.services.analytics_service import AnalyticsService
from app.services.loan_service import LoanService

report_bp = Blueprint('report', __name__)

@report_bp.route('/details', methods=['GET'])
@jwt_required()
def report_details():
    user_id = get_jwt_identity()
    score_data = ScoreService.calculate_user_score(user_id)
    
    # Generate suggestions based on breakdown
    suggestions = []
    if score_data['breakdown']['margin'] < 20:
        suggestions.append("Improve profit margins by reviewing pricing.")
    if score_data['breakdown']['stability'] < 30:
        suggestions.append("Focus on consistent cash flow to improve stability.")
    if score_data['breakdown']['control'] < 20:
        suggestions.append("Reduce overhead expenses to improve control score.")
    
    score_data['suggestions'] = suggestions
    return jsonify(score_data)

@report_bp.route('/loan', methods=['GET'])
@jwt_required()
def loan_status():
    user_id = get_jwt_identity()
    score_data = ScoreService.calculate_user_score(user_id)
    loan_info = LoanService.check_eligibility(score_data)
    return jsonify(loan_info)

@report_bp.route('/monthly', methods=['GET'])
@jwt_required()
def monthly_report():
    user_id = get_jwt_identity()
    report = AnalyticsService.get_monthly_report(user_id)
    return jsonify(report)