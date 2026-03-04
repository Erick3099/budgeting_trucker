from abc import ABC, abstractmethod

class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, income: float) -> float:
        pass


class FlatTax(TaxStrategy):
    def calculate(self, income: float) -> float:
        return income * 0.10


class ProgressiveTax(TaxStrategy):
    def calculate(self, income: float) -> float:
        if income <= 3000:
            return income * 0.05
        elif income <= 6000:
            return income * 0.15
        return income * 0.25