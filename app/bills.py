import os
import json
from app.models import BudgetVault, Bill

DATA_FILE = "data/budget_data.json"


def ensure_data_directory():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def save_budget(vault: BudgetVault, filepath: str = DATA_FILE) -> bool:
    try:
        ensure_data_directory()

        data = {
            "salary": float(getattr(vault, "salary", 0.0)),
            "transactions": []
        }

        for transaction in vault.get_all_transactions():
            data["transactions"].append({
                "name": transaction.name,
                "amount": float(transaction.amount),
                "is_fixed": bool(getattr(transaction, "is_fixed", False))
            })

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return True

    except PermissionError:
        print(f"ERROR: Permission denied when writing to {filepath}")
        return False

    except IOError as e:
        print(f"ERROR: File write failed: {e}")
        return False

    except Exception as e:
        print(f"UNEXPECTED ERROR while saving: {e}")
        return False


def load_budget(filepath: str = DATA_FILE) -> BudgetVault:
    vault = BudgetVault()

    if not os.path.exists(filepath):
        return vault

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        
        vault.salary = float(data.get("salary", 0.0))

    
        for item in data.get("transactions", []):
            bill = Bill(
                name=item.get("name", "Unnamed"),
                amount=float(item.get("amount", 0.0)),
                is_fixed=bool(item.get("is_fixed", False))
            )
            vault.add_transaction(bill)

        return vault

    except json.JSONDecodeError:
        print("ERROR: Corrupted JSON file. Creating backup and starting fresh.")

        backup_path = filepath + ".backup"
        try:
            import shutil
            shutil.copy(filepath, backup_path)
            print(f"Backup created at {backup_path}")
        except Exception:
            pass

        return BudgetVault()

    except PermissionError:
        print(f"ERROR: Permission denied when reading {filepath}")
        return BudgetVault()

    except Exception as e:
        print(f"UNEXPECTED ERROR while loading: {e}")
        return BudgetVault()