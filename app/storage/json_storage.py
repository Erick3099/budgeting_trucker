import json
import os
from typing import List
from app.models import Bill

class JSONStorage:
    def __init__(self, filepath: str = "data/budget_data.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def save(self, username: str, income: float, bills: List[Bill]):
        data = {
            "username": username,
            "income": income,
            "bills": [
                {
                    "name": bill.name,
                    "amount": bill.amount,
                    "is_fixed": bill.is_fixed
                }
                for bill in bills
            ]
        }

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filepath):
            return None

        with open(self.filepath, "r") as f:
            return json.load(f)