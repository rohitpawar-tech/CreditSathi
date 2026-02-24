class LoanService:
    @staticmethod
    def check_eligibility(score_data):
        # Criteria
        score = score_data['total_score']
        profit = score_data['financials']['profit']
        sales = score_data['financials']['sales']
        expenses = score_data['financials']['expenses']

        checks = {
            "high_score": score >= 75,
            "positive_profit": profit > 0,
            "expense_ratio": False
        }

        if sales > 0:
            checks["expense_ratio"] = (expenses / sales) < 0.8

        is_eligible = all(checks.values())

        return {
            "eligible": is_eligible,
            "checks": checks,
            "status": "Approved" if is_eligible else "Rejected",
            "message": "Business meets lending criteria" if is_eligible else "Improve financial metrics"
        }