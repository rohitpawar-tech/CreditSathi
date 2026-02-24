from app.extensions import db  # <--- IMPORTANT LINE ADDED
from app.models.sale import Sale
from app.models.expense import Expense
from sqlalchemy import func

class AnalyticsService:
    @staticmethod
    def get_monthly_report(user_id):
        # Note: This is a simplified aggregation. 
        # Production code would use complex SQL date_trunc for precise grouping.
        
        sales_data = db.session.query(
            func.strftime('%Y-%m', Sale.date).label('month'),
            func.sum(Sale.amount).label('total')
        ).filter_by(user_id=user_id).group_by('month').all()

        expense_data = db.session.query(
            func.strftime('%Y-%m', Expense.date).label('month'),
            func.sum(Expense.amount).label('total')
        ).filter_by(user_id=user_id).group_by('month').all()

        report = {}
        
        # Process Sales
        for s in sales_data:
            report[s.month] = {"month": s.month, "sales": float(s.total), "expenses": 0.0}

        # Process Expenses
        for e in expense_data:
            if e.month in report:
                report[e.month]["expenses"] = float(e.total)
            else:
                report[e.month] = {"month": e.month, "sales": 0.0, "expenses": float(e.total)}

        # Calculate Profit and Sort
        final_report = []
        for k, v in report.items():
            v["profit"] = v["sales"] - v["expenses"]
            final_report.append(v)
        
        return sorted(final_report, key=lambda x: x['month'], reverse=True)