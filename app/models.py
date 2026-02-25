from typing import List

class Transaction:
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = float(amount)

class Bill(Transaction):
    def __init__(self, name: str, amount: float, is_fixed: bool = False):
        super().__init__(name, amount)
        self.is_fixed = is_fixed

class BudgetVault:
    def __init__(self):
        self._transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("Must be a Transaction or Bill instance")
        self._transactions.append(transaction)

    def get_all_transactions(self) -> List[Transaction]:
        return self._transactions

    def get_total(self) -> float:
        return sum(t.amount for t in self._transactions)