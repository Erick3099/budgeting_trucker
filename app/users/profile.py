from app.models import BudgetVault

class UserProfile:
    def __init__(self, username: str, monthly_income: float):
        self.username = username
        self.monthly_income = float(monthly_income)
        self.vault = BudgetVault()

    def add_bill(self, bill):
        self.vault.add_transaction(bill)

    def get_total_expenses(self):
        return self.vault.get_total()