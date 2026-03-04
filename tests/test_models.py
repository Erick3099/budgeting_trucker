from app.models import Bill, BudgetVault

def test_add_transaction():
    vault = BudgetVault()
    bill = Bill("Rent", 1000, True)
    vault.add_transaction(bill)
    assert vault.get_total() == 1000

def test_multiple_transactions():
    vault = BudgetVault()
    vault.add_transaction(Bill("Rent", 1000))
    vault.add_transaction(Bill("Food", 500))
    assert vault.get_total() == 1500