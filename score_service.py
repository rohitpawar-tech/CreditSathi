from app.extensions import db  # <--- IMPORTANT LINE ADDED
from app.models.sale import Sale
from app.models.expense import Expense
from sqlalchemy import func, extract
from datetime import datetime, timedelta

class ScoreService:
    @staticmethod
    def calculate_user_score(user_id):
        # Aggregates
        total_sales = db.session.query(func.sum(Sale.amount)).filter_by(user_id=user_id).scalar() or 0
        total_expenses = db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0
        profit = total_sales - total_expenses

        # 1. Profit Margin Score (Max 40)
        margin_score = 0
        if total_sales > 0:
            margin_percent = (profit / total_sales) * 100
            if margin_percent > 20:
                margin_score = 40
            else:
                margin_score = max(0, (margin_percent / 20) * 40)

        # 2. Cash Flow Stability (Max 30) - Based on last 3 months trend vs avg
        stability_score = 0
        # Simplified: If profitable
        if profit > 0:
            stability_score = 30
        
        # 3. Expense Control (Max 30) - Expense Ratio
        control_score = 0
        if total_sales > 0:
            expense_ratio = total_expenses / total_sales
            if expense_ratio < 0.6:
                control_score = 30
            elif expense_ratio < 0.85:
                control_score = 15
            else:
                control_score = 5

        total_score = round(margin_score + stability_score + control_score)
        
        # Risk Badge Logic
        risk_level = "Risky"
        if total_score >= 75: risk_level = "Healthy"
        elif total_score >= 45: risk_level = "Average"

        return {
            "total_score": total_score,
            "breakdown": {
                "margin": round(margin_score),
                "stability": round(stability_score),
                "control": round(control_score)
            },
            "financials": {
                "sales": total_sales,
                "expenses": total_expenses,
                "profit": profit
            },
            "risk": risk_level
        }