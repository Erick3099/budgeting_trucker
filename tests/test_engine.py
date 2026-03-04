import pytest
from app.engine import flat_tax_logic, progressive_tax_logic, run_budget_analysis

def test_flat_tax():
    assert flat_tax_logic(1000) == 100

def test_progressive_tax_low():
    assert progressive_tax_logic(2000) == 100

def test_progressive_tax_mid():
    assert progressive_tax_logic(5000) == 750

def test_progressive_tax_high():
    assert progressive_tax_logic(10000) == 2500

def test_budget_analysis():
    income = 5000
    expenses = [500, 500]
    result = run_budget_analysis(income, expenses, flat_tax_logic)
    assert result == 5000 - 500 - 1000